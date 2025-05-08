// Import diff library for parsing and applying unified diffs
import { parsePatch, applyPatch } from 'diff';

/**
 * Converts escape sequences in a string to their actual characters
 * This handles common escape sequences like \n, \t, \r, etc.
 * Also normalizes line endings to ensure consistent processing
 */
export function convertEscapeSequences(input: string): string {
    if (!input) return input;

    // Convert escape sequences
    const withConvertedEscapes = input
        .replace(/\\n/g, '\n')   // Convert \n to actual newlines
        .replace(/\\t/g, '\t')   // Convert \t to actual tabs
        .replace(/\\r/g, '\r')   // Convert \r to actual carriage returns
        .replace(/\\\\/g, '\\')  // Convert \\ to single backslash
        .replace(/\\"/g, '"')    // Convert \" to double quote
        .replace(/\\'/g, "'");   // Convert \' to single quote

    // Normalize line endings (convert \r\n to \n)
    return withConvertedEscapes.replace(/\r\n/g, '\n');
}

/**
 * Preprocesses a diff to ensure it's in a format that jsdiff can parse
 * This handles issues with hunk headers and ensures all lines have proper prefixes
 */
export function preprocessDiff(diff: string): string {
    if (!diff) return '';

    // Split the diff into lines
    const lines = diff.split('\n');

    // Extract file headers (lines starting with --- or +++)
    const fileHeaders = [];
    for (const line of lines) {
        if (line.startsWith('---') || line.startsWith('+++')) {
            fileHeaders.push(line);
        }
    }

    // Create a completely new diff with proper formatting
    const result = [];

    // Add file headers
    if (fileHeaders.length > 0) {
        result.push(...fileHeaders);
    } else {
        // Add default file headers if none exist
        result.push('--- a');
        result.push('+++ b');
    }

    // Extract added and removed lines
    const addedLines = [];
    const removedLines = [];

    for (const line of lines) {
        if (line.startsWith('+') && !line.startsWith('+++')) {
            addedLines.push(line.substring(1));
        } else if (line.startsWith('-') && !line.startsWith('---')) {
            removedLines.push(line.substring(1));
        }
    }

    // Create a simple hunk header
    result.push('@@ -1,0 +1,' + addedLines.length + ' @@');

    // Add the added lines with '+' prefix
    for (const line of addedLines) {
        result.push('+' + line);
    }

    return result.join('\n');
}

/**
 * Result of applying a diff to content
 */
export interface DiffResult {
    /** The patched content */
    content: string;
    /** Any errors that occurred during patching */
    errors: string[];
    /** Whether the patching was successful */
    success: boolean;
}

/**
 * Applies a diff to the original content and returns the patched content
 * @param originalContent The original content to apply the diff to
 * @param diff The diff to apply (in unified diff format)
 * @param silent Whether to suppress error logging (default: false)
 * @returns The patched content
 */
export function applyDiffToContent(originalContent: string, diff: string, silent: boolean = false): string {
    if (!diff) return originalContent;

    try {
        // Convert escape sequences in the diff string
        const withEscapesConverted = convertEscapeSequences(diff);

        if (!silent) {
            console.log('DEBUG - Original diff:');
            console.log(diff);
            console.log('DEBUG - After escape conversion:');
            console.log(withEscapesConverted);
        }

        // Use the diff library's parsePatch and applyPatch functions
        try {
            const patches = parsePatch(withEscapesConverted);

            if (patches.length === 0) {
                if (!silent) {
                    console.log('DEBUG - No patches found in diff');
                }
                return originalContent;
            }

            // Apply each patch to the content
            let result = originalContent;
            for (const patch of patches) {
                try {
                    const patchResult = applyPatch(result, patch);
                    if (patchResult) {
                        result = patchResult;
                    }
                } catch (err) {
                    if (!silent) {
                        console.error(`DEBUG - Error applying patch: ${err instanceof Error ? err.message : String(err)}`);
                    }
                    // Fall back to direct application if patch fails
                    return applyDiffDirectly(originalContent, withEscapesConverted, silent);
                }
            }

            if (!silent) {
                console.log('DEBUG - Successfully applied patches');
                console.log('DEBUG - Result:', result);
            }

            return result;
        } catch (err) {
            if (!silent) {
                console.error(`DEBUG - Error parsing patch: ${err instanceof Error ? err.message : String(err)}`);
            }
            // Fall back to direct application if parsing fails
            return applyDiffDirectly(originalContent, withEscapesConverted, silent);
        }
    } catch (err) {
        if (!silent) {
            console.error(`DEBUG - Unexpected error: ${err instanceof Error ? err.message : String(err)}`);
        }
        return originalContent;
    }
}

/**
 * Applies a diff directly by extracting added and removed lines
 * This is a fallback method when the diff library fails
 * 
 * @param originalContent The original content to apply the diff to
 * @param diff The diff to apply
 * @param silent Whether to suppress error logging
 * @returns The patched content
 */
function applyDiffDirectly(originalContent: string, diff: string, silent: boolean = false): string {
    if (!silent) {
        console.log('DEBUG - Falling back to direct diff application');
    }

    // Split content and diff into lines
    const originalLines = originalContent.split('\n');
    const diffLines = diff.split('\n');

    // Parse the hunk header to get line numbers
    let hunkHeader = diffLines.find(line => line.startsWith('@@'));
    if (!hunkHeader) {
        // If no hunk header, just extract added lines and prepend them
        const addedLines = diffLines
            .filter(line => line.startsWith('+') && !line.startsWith('+++'))
            .map(line => line.substring(1));

        if (addedLines.length === 0) {
            return originalContent;
        }

        // Create a new array with the modified content
        const resultLines = [...addedLines, ...originalLines];

        if (!silent) {
            console.log('DEBUG - Direct application added lines:', addedLines.length);
        }

        return resultLines.join('\n');
    }

    // Try to parse the hunk header
    const hunkMatch = hunkHeader.match(/@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@/);
    if (!hunkMatch) {
        // If can't parse hunk header, fall back to simple addition
        const addedLines = diffLines
            .filter(line => line.startsWith('+') && !line.startsWith('+++'))
            .map(line => line.substring(1));

        if (addedLines.length === 0) {
            return originalContent;
        }

        // Create a new array with the modified content
        const resultLines = [...addedLines, ...originalLines];

        if (!silent) {
            console.log('DEBUG - Direct application added lines (no hunk match):', addedLines.length);
        }

        return resultLines.join('\n');
    }

    // Parse hunk header
    const oldStart = parseInt(hunkMatch[1], 10);
    const oldLines = hunkMatch[2] ? parseInt(hunkMatch[2], 10) : 1;

    // Get the context lines (lines that start with ' '), added lines ('+'), and removed lines ('-')
    const hunkLines = diffLines.filter(line =>
        line.startsWith(' ') ||
        (line.startsWith('+') && !line.startsWith('+++')) ||
        (line.startsWith('-') && !line.startsWith('---'))
    );

    // Apply the changes
    const resultLines = [...originalLines];
    let lineIndex = oldStart - 1; // 0-based index
    let hunkIndex = 0;

    while (hunkIndex < hunkLines.length) {
        const line = hunkLines[hunkIndex];

        if (line.startsWith(' ')) {
            // Context line - just move to next line
            lineIndex++;
            hunkIndex++;
        } else if (line.startsWith('-')) {
            // Remove line
            if (lineIndex < resultLines.length) {
                resultLines.splice(lineIndex, 1);
            }
            hunkIndex++;
        } else if (line.startsWith('+')) {
            // Add line
            resultLines.splice(lineIndex, 0, line.substring(1));
            lineIndex++;
            hunkIndex++;
        }
    }

    if (!silent) {
        console.log('DEBUG - Applied hunk changes directly');
    }

    return resultLines.join('\n');
}
