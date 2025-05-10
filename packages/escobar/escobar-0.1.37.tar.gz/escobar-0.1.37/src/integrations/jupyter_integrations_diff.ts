import { JupyterFrontEnd } from '@jupyterlab/application';
import { app, functions } from './jupyter_integrations';
import { streamingState } from "./jupyter_integrations";
import { CodeMirrorEditor, jupyterTheme, jupyterHighlightStyle } from '@jupyterlab/codemirror';
import { Widget } from '@lumino/widgets';

// Import necessary CodeMirror modules
import { StateEffect, StateField, EditorState, Text, Extension, Compartment } from '@codemirror/state';
import { Decoration, EditorView, ViewPlugin } from '@codemirror/view';
import { MergeView } from '@codemirror/merge';
import { LanguageSupport, syntaxHighlighting } from '@codemirror/language';

// Import language support modules
import { python } from '@codemirror/lang-python';
import { javascript } from '@codemirror/lang-javascript';
import { json } from '@codemirror/lang-json';
import { markdown } from '@codemirror/lang-markdown';
import { html } from '@codemirror/lang-html';
import { css } from '@codemirror/lang-css';

// Import diff utilities from the module
import { applyDiffToContent, unescapeString, fixPartialDiff } from '../utils/diff-utils';

// Debug function to log information about the editor state
function debugEditorState(editor: EditorView, label: string) {
    console.log(`Debug ${label}:`, {
        hasFocus: editor.hasFocus,
        docLength: editor.state.doc.length
    });
}

// Function to get language extensions for a file based on its extension
function getLanguageExtensionsForFile(filePath: string): Extension[] {
    const fileExtension = filePath.split('.').pop()?.toLowerCase() || '';
    const extensions: Extension[] = [];

    // Always add JupyterLab's syntax highlighting
    extensions.push(syntaxHighlighting(jupyterHighlightStyle));

    // Add language support based on file extension
    let languageSupport: Extension | null = null;

    switch (fileExtension) {
        case 'py':
            languageSupport = python();
            break;
        case 'js':
            languageSupport = javascript();
            break;
        case 'ts':
            languageSupport = javascript({ typescript: true });
            break;
        case 'jsx':
            languageSupport = javascript({ jsx: true });
            break;
        case 'tsx':
            languageSupport = javascript({ jsx: true, typescript: true });
            break;
        case 'json':
            languageSupport = json();
            break;
        case 'md':
            languageSupport = markdown();
            break;
        case 'html':
        case 'htm':
            languageSupport = html();
            break;
        case 'css':
            languageSupport = css();
            break;
        // Add more language support as needed
    }

    if (languageSupport) {
        extensions.push(languageSupport);
        console.log(`Added language support for ${fileExtension}`);
    } else {
        console.log(`No specific language support for ${fileExtension}, using default highlighting`);
    }

    return extensions;
}

var mergeViews = {};
var mergeWidgets = {}

export function init_diff() {
    functions["diffToFile"] = {
        "def": {
            "name": "diffToFile",
            "description": "Apply unified diff to a file. Unified diff format only! Make sure to conform with the diff format! Important: include line numbers in the Honk header",
            "arguments": {
                "filePath": {
                    "type": "string",
                    "name": "Relative path to the file to display in merge view. Relative! "
                },
                "diff": {
                    "type": "string",
                    "name": "Unified diff content to apply to the file (must be in unified diff format, with line numbers in Honk header)"
                }
            }
        },
        "func": async (args: any, streaming: boolean = false, call_id: string = undefined): Promise<string> => {
            // Function to apply syntax highlighting directly to the editors
            function updateDocB(mergeView: MergeView, newContent: string): boolean {
                try {
                    // Try to access the editor for doc B directly through the mergeView object
                    if (!mergeView.b || !mergeView.b.state) {
                        console.error('Could not access state for doc B');
                        return false;
                    }

                    // Get the current state and create a new state with the updated content
                    const currentState = mergeView.b.state;

                    // Create a transaction to replace the entire document content
                    mergeView.b.dispatch({
                        changes: {
                            from: 0,
                            to: currentState.doc.length,
                            insert: newContent
                        }
                    });

                    console.log('Successfully updated doc B');
                    return true;
                } catch (err) {
                    console.error('Error updating doc B:', err);
                    return false;
                }
            }




            const applySyntaxHighlighting = (mergeView) => {
                try {
                    const editors = mergeView.dom.querySelectorAll('.cm-editor');
                    console.log(`Found ${editors.length} editors in merge view`);

                    editors.forEach((editorElement, index) => {
                        const editorView = (editorElement as any).view;
                        if (editorView) {
                            debugEditorState(editorView, `Editor ${index}`);

                            // Add a class to the editor element based on file extension
                            const fileExtension = filePath.split('.').pop()?.toLowerCase() || '';
                            editorElement.classList.add(`language-${fileExtension}`);

                            // Force a refresh of the editor view
                            setTimeout(() => {
                                try {
                                    // Dispatch a dummy transaction to force a refresh
                                    editorView.dispatch({});
                                } catch (err) {
                                    console.error(`Error refreshing editor ${index}:`, err);
                                }
                            }, 100);
                        } else {
                            console.log(`Could not access view for editor ${index}`);
                        }
                    });
                } catch (err) {
                    console.error("Error applying syntax highlighting:", err);
                }
            };



            if (!app) {
                return JSON.stringify({ error: "JupyterLab app not initialized" });
            }

            const { contents } = app.serviceManager;
            const { filePath, diff } = args;

            try {
                // Read the file content
                let fileContent;
                try {
                    fileContent = await contents.get(filePath);
                } catch (err) {
                    return JSON.stringify({
                        "status": "fail",
                        "message": `Cannot open file: ${filePath} does not exist`
                    });
                }

                const originalContent = fileContent.content as string;

                console.log('DEBUG - Original content length:', originalContent.length);
                console.log('DEBUG - Diff provided:', !!diff);
                if (diff) {
                    console.log('DEBUG - Diff length:', diff.length);
                }

                // Apply the diff to get the patched content
                // We'll use false for silent to see debug logs
                // Use the options parameter to control unescaping and fixing partial diffs
                const options = {
                    unescape: true,
                    fixPartial: streaming  // Only fix partial diffs if streaming is true
                };

                // Apply the diff with the specified options
                const patchedContent = diff ? applyDiffToContent(originalContent, diff, false, options) : originalContent;

                // For debugging, also apply without fixing partial diffs
                const optionsNoFix = {
                    unescape: true,
                    fixPartial: false
                };
                const patchedContent0 = diff ? applyDiffToContent(originalContent, diff, false, optionsNoFix) : originalContent;

                const originalLength = originalContent.length;
                const patchedLength = patchedContent.length;
                const patchedLength0 = patchedContent0.length;

                if ((originalLength != patchedLength) || (originalLength != patchedLength0)) {
                    //alert(`${originalLength} ${patchedLength} ${patchedLength0}`)
                }

                console.log('DEBUG - Original content length:', originalLength);
                console.log('DEBUG - Patched content length (fixed diff):', patchedLength);
                console.log('DEBUG - Patched content length (original diff):', patchedLength0);
                console.log('DEBUG - Content changed (fixed diff):', patchedContent !== originalContent);
                console.log('DEBUG - Content changed (original diff):', patchedContent0 !== originalContent);
                console.log('DEBUG - Fixed diff and original diff produce same result:', patchedContent === patchedContent0);


                if (mergeViews[call_id] != undefined) {
                    updateDocB(mergeViews[call_id], patchedContent);
                } else if (mergeViews[call_id] == undefined) {

                    // Create a container for the merge view
                    const container = document.createElement('div');
                    container.style.height = '100%';
                    container.style.overflow = 'auto';

                    // Get language extensions for the file and add JupyterLab theme
                    const languageExtensions = [jupyterTheme, ...getLanguageExtensionsForFile(filePath)];

                    // Add a style element for syntax highlighting using JupyterLab's CSS variables
                    const styleElement = document.createElement('style');
                    styleElement.textContent = `
                        /* Basic syntax highlighting styles using JupyterLab variables */
                        .cm-keyword { color: var(--jp-mirror-editor-keyword-color); font-weight: bold; }
                        .cm-comment { color: var(--jp-mirror-editor-comment-color); }
                        .cm-string { color: var(--jp-mirror-editor-string-color); }
                        .cm-number { color: var(--jp-mirror-editor-number-color); }
                        .cm-operator { color: var(--jp-mirror-editor-operator-color); }
                        .cm-property { color: var(--jp-mirror-editor-property-color); }
                        .cm-variable { color: var(--jp-mirror-editor-variable-color); }
                        .cm-function, .cm-def { color: var(--jp-mirror-editor-def-color); }
                        .cm-atom { color: var(--jp-mirror-editor-atom-color); }
                        .cm-meta { color: var(--jp-mirror-editor-meta-color); }
                        .cm-tag { color: var(--jp-mirror-editor-tag-color); }
                        .cm-attribute { color: var(--jp-mirror-editor-attribute-color); }
                        .cm-qualifier { color: var(--jp-mirror-editor-qualifier-color); }
                        .cm-bracket { color: var(--jp-mirror-editor-bracket-color); }
                        .cm-builtin { color: var(--jp-mirror-editor-builtin-color); }
                        .cm-special { color: var(--jp-mirror-editor-string-2-color); }
                    `;
                    document.head.appendChild(styleElement);

                    const mergeView = new MergeView({
                        a: {
                            doc: originalContent,
                            extensions: languageExtensions
                        },
                        b: {
                            doc: patchedContent,
                            extensions: languageExtensions
                        },
                        highlightChanges: true
                    });


                    mergeViews[call_id] = mergeView;

                    container.appendChild(mergeView.dom);

                    setTimeout(function () {
                        applySyntaxHighlighting(mergeView);
                    }, 500);

                    // Create a widget to hold the container
                    const widget = new Widget();
                    mergeWidgets[call_id] = widget;

                    widget.id = call_id;
                    widget.title.label = `Merge View: ${filePath}`;
                    widget.title.closable = true;
                    widget.node.appendChild(container);

                    // Add the widget to the main area and activate it
                    app.shell.add(widget, 'main');
                    app.shell.activateById(widget.id);

                }

                if (!streaming) {
                    console.log(app.commands.listCommands());

                    //app.commands.execute('docmanager:close', { path: filePath });

                    await contents.save(filePath, {
                        type: 'file',
                        format: 'text',
                        content: patchedContent
                    });

                    // Close the merge view widget if it exists
                    if (mergeViews[call_id]) {
                        // Find the widget by ID and close it
                        const widget = mergeWidgets[call_id];
                        //const widget = app.shell.widgets('main').find(w => w.id === call_id);
                        if (widget) {
                            setTimeout(() => {
                                widget.close();
                                setTimeout(() => {
                                    app.commands.execute('docmanager:open', { path: filePath });
                                    setTimeout(() => {
                                        app.commands.execute('docmanager:reload')
                                    }, 100)
                                }, 100)
                            }, 1000);
                        }
                    }
                }

                return JSON.stringify({
                    "status": "ok",
                    "message": "Merge view opened successfully"
                });
            } catch (err) {
                return JSON.stringify({
                    "status": "fail",
                    "message": `Failed to open merge view: ${err.message}`
                });
            }
        }
    }
}
