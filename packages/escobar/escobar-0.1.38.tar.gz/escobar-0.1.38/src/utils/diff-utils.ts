/**
 * Utility functions for handling diffs
 * Based on the PatchCraft approach which combines parse-diff and diff-match-patch
 */

/**
 * Unescapes string escape sequences
 * @param input - The string to unescape
 * @returns The unescaped string
 */
export function unescapeString(input: string): string {
    if (!input) return input;

    // First handle the standard escape sequences
    let result = input
        .replace(/\\n/g, '\n')       // newline
        .replace(/\\r/g, '\r')       // carriage return
        .replace(/\\t/g, '\t')       // tab
        .replace(/\\b/g, '\b')       // backspace
        .replace(/\\f/g, '\f')       // form feed
        .replace(/\\v/g, '\v')       // vertical tab
        .replace(/\\\\/g, '\\')      // backslash
        .replace(/\\"/g, '"')        // double quote
        .replace(/\\'/g, "'");       // single quote

    // Handle hex escapes (\xXX)
    result = result.replace(/\\x([0-9A-Fa-f]{2})/g, (_, hex) =>
        String.fromCharCode(parseInt(hex, 16))
    );

    // Handle unicode escapes (\uXXXX)
    result = result.replace(/\\u([0-9A-Fa-f]{4})/g, (_, hex) =>
        String.fromCharCode(parseInt(hex, 16))
    );

    // Handle unicode code point escapes (\u{XXXXX})
    result = result.replace(/\\u\{([0-9A-Fa-f]+)\}/g, (_, hex) =>
        String.fromCodePoint(parseInt(hex, 16))
    );

    // Handle null character escape (\0)
    result = result.replace(/\\0/g, '\0');

    // Normalize line endings (convert \r\n to \n)
    result = result.replace(/\r\n/g, '\n');

    return result;
}

/**
 * Fixes partial diffs to ensure they are properly formatted
 * @param diff - The diff content to fix
 * @returns The fixed diff content
 */
export function fixPartialDiff(diff: string): string {
    const lines = diff.split('\n');
    const cleanedLines: string[] = [];
    let insideHunk = false;

    for (const line of lines) {
        // Skip empty lines
        if (line.trim() === '') {
            continue;
        }

        // Pass through file headers and valid hunk headers unchanged
        if (line.startsWith('---') || line.startsWith('+++')) {
            cleanedLines.push(line);
            continue;
        }

        // Handle hunk headers
        if (line.startsWith('@@')) {
            // Skip placeholder hunk headers like "@@ ... @@"
            if (line.includes('...')) {
                continue;
            }

            // Valid hunk header
            cleanedLines.push(line);
            insideHunk = true;
            continue;
        }

        // Inside a hunk, only keep lines with proper prefixes
        if (insideHunk) {
            if (line.startsWith('+') || line.startsWith('-') || line.startsWith(' ')) {
                cleanedLines.push(line);
            }
            // Skip lines without proper prefixes
        } else {
            // Not inside a hunk, just add the line
            cleanedLines.push(line);
        }
    }

    return cleanedLines.join('\n');
}

/**
 * Applies a diff to content
 * @param originalContent - The original content
 * @param diff - The diff to apply
 * @param silent - Whether to suppress console logs
 * @param options - Options for applying the diff
 * @returns The content after applying the diff
 */
export function applyDiffToContent(
    originalContent: string,
    diff: string,
    silent: boolean = true,
    options: {
        unescape?: boolean,
        fixPartial?: boolean
    } = {}
): string {
    // Process options with defaults
    const opts = {
        unescape: options.unescape !== undefined ? options.unescape : true,
        fixPartial: options.fixPartial !== undefined ? options.fixPartial : true
    };

    // Apply preprocessing based on options
    let processedDiff = diff;

    if (opts.unescape) {
        processedDiff = unescapeString(processedDiff);
        if (!silent) {
            console.log('Applied unescapeString to diff');
        }
    }

    if (opts.fixPartial) {
        processedDiff = fixPartialDiff(processedDiff);
        if (!silent) {
            console.log('Applied fixPartialDiff to diff');
        }
    }

    // Special case: If the diff has no valid chunks after parsing or if it contains "@@ ... @@",
    // try a more direct approach. This handles cases where the diff format is non-standard
    // but still follows basic +/- line prefixes
    if (!processedDiff.includes('@@ -') || processedDiff.includes('@@ ... @@')) {
        if (!silent) {
            console.log('Non-standard hunk headers found, trying direct line-by-line processing');
        }
        return applySimpleDiff(originalContent, processedDiff, silent);
    }

    // Split the original content and diff into lines
    const originalLines = originalContent.split('\n');
    const diffLines = processedDiff.split('\n');

    // Create a copy of the original lines that we'll modify
    let modifiedLines = [...originalLines];

    // Parse the diff to extract chunks
    const chunks: any[] = [];
    let currentChunk: any = null;

    for (const line of diffLines) {
        if (line.startsWith('@@')) {
            // Parse the hunk header to get line numbers
            // Format: @@ -oldStart,oldCount +newStart,newCount @@
            // Some diffs might have just @@ without line numbers
            const match = line.match(/@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@/);

            if (match) {
                const oldStart = parseInt(match[1], 10);
                const oldCount = match[2] ? parseInt(match[2], 10) : 1;

                if (currentChunk) {
                    chunks.push(currentChunk);
                }

                currentChunk = {
                    oldStart,
                    oldCount,
                    changes: []
                };
            } else {
                // Handle the case where the hunk header doesn't have line numbers
                if (!silent) {
                    console.log('Hunk header without line numbers detected, using default values');
                }

                if (currentChunk) {
                    chunks.push(currentChunk);
                }

                // Use default values: start at line 1 with a count of 1
                currentChunk = {
                    oldStart: 1,
                    oldCount: 1,
                    changes: []
                };
            }
        } else if (currentChunk) {
            if (line.startsWith('+') || line.startsWith('-') || line.startsWith(' ')) {
                // Add the change to the current chunk
                currentChunk.changes.push({
                    type: line.startsWith('+') ? 'add' : line.startsWith('-') ? 'del' : 'normal',
                    content: line.substring(1)
                });
            } else if (line.trim() !== '') {
                // Handle lines without a prefix (treat as context lines)
                // This is common in diffs without line numbers
                if (!silent) {
                    console.log(`Line without prefix detected: "${line}"`);
                }
                currentChunk.changes.push({
                    type: 'add',  // Treat as an addition
                    content: line
                });
            }
        }
    }

    if (currentChunk) {
        chunks.push(currentChunk);
    }

    if (!silent) {
        console.log(`Parsed ${chunks.length} chunks from diff`);
    }

    // Process chunks in reverse order to avoid line number changes affecting subsequent chunks
    for (let i = chunks.length - 1; i >= 0; i--) {
        const chunk = chunks[i];

        // The line where changes start (0-based)
        const lineIndex = chunk.oldStart - 1;

        if (!silent) {
            console.log(`Processing chunk ${i + 1}/${chunks.length}, starting at line ${lineIndex + 1}`);
        }

        // Extract the changes
        const changes = chunk.changes;

        // Group consecutive additions and deletions
        const changeGroups: any[] = [];
        let currentGroup: any = null;

        for (const change of changes) {
            if (change.type === 'normal') {
                if (currentGroup) {
                    changeGroups.push(currentGroup);
                    currentGroup = null;
                }
            } else {
                if (!currentGroup || currentGroup.type !== change.type) {
                    if (currentGroup) {
                        changeGroups.push(currentGroup);
                    }
                    currentGroup = {
                        type: change.type,
                        changes: [change]
                    };
                } else {
                    currentGroup.changes.push(change);
                }
            }
        }

        if (currentGroup) {
            changeGroups.push(currentGroup);
        }

        if (!silent) {
            console.log(`Found ${changeGroups.length} change groups`);
            changeGroups.forEach((group, idx) => {
                console.log(`Group ${idx + 1}: type=${group.type}, changes=${group.changes.length}`);
            });
        }

        // Apply change groups in reverse order
        for (let j = changeGroups.length - 1; j >= 0; j--) {
            const group = changeGroups[j];

            // Find the position of this group in the chunk
            let position = 0;
            for (const change of changes) {
                if (change === group.changes[0]) {
                    break;
                }
                if (change.type === 'normal' || change.type === 'del') {
                    position++;
                }
            }

            if (!silent) {
                console.log(`Applying group ${j + 1}: type=${group.type}, position=${position}, changes=${group.changes.length}`);
                if (group.type === 'del') {
                    console.log(`Removing ${group.changes.length} lines at position ${lineIndex + position}`);
                    group.changes.forEach((change: any, idx: number) => {
                        console.log(`  Line ${idx + 1} to remove: "${change.content}"`);
                    });
                } else if (group.type === 'add') {
                    console.log(`Adding ${group.changes.length} lines at position ${lineIndex + position}`);
                    group.changes.forEach((change: any, idx: number) => {
                        console.log(`  Line ${idx + 1} to add: "${change.content}"`);
                    });
                }
            }

            if (group.type === 'del') {
                // Remove lines one by one to ensure correct handling
                for (let k = 0; k < group.changes.length; k++) {
                    // Always remove from the same position since the array shifts after each removal
                    modifiedLines.splice(lineIndex + position, 1);
                    if (!silent) {
                        console.log(`  Removed line at position ${lineIndex + position}, modifiedLines.length=${modifiedLines.length}`);
                    }
                }
            } else if (group.type === 'add') {
                // Add lines
                const linesToAdd = group.changes.map((change: any) => change.content);
                modifiedLines.splice(lineIndex + position, 0, ...linesToAdd);
            }

            if (!silent) {
                console.log(`After applying group ${j + 1}, modifiedLines.length=${modifiedLines.length}`);
            }
        }
    }

    // Join the modified lines back into a string
    return modifiedLines.join('\n');
}

/**
 * Applies a simple diff directly, line by line
 * This is used for non-standard diffs that don't have proper hunk headers
 * @param originalContent - The original content
 * @param diff - The diff to apply
 * @param silent - Whether to suppress console logs
 * @returns The content after applying the diff
 */
export function applySimpleDiff(originalContent: string, diff: string, silent: boolean = true): string {
    // Split the original content and diff into lines
    const originalLines = originalContent.split('\n');
    const diffLines = diff.split('\n');

    // Create a new array for the result
    let resultLines: string[] = [];

    // Skip file headers and hunk headers
    let startIndex = 0;
    while (startIndex < diffLines.length &&
        (diffLines[startIndex].startsWith('---') ||
            diffLines[startIndex].startsWith('+++') ||
            diffLines[startIndex].startsWith('@@') ||
            diffLines[startIndex].trim() === '')) {
        startIndex++;
    }

    // Process the diff lines
    let inRemovedBlock = false;
    let inAddedBlock = false;
    let removedLines: string[] = [];
    let addedLines: string[] = [];

    // First pass: collect all removed and added lines
    for (let i = startIndex; i < diffLines.length; i++) {
        const line = diffLines[i];

        if (line.startsWith('-')) {
            // Line to remove
            removedLines.push(line.substring(1));
            inRemovedBlock = true;

            // If we were in an added block, process it
            if (inAddedBlock) {
                inAddedBlock = false;
            }
        } else if (line.startsWith('+')) {
            // Line to add
            addedLines.push(line.substring(1));
            inAddedBlock = true;

            // If we were in a removed block, process it
            if (inRemovedBlock) {
                inRemovedBlock = false;
            }
        } else if (line.trim() !== '') {
            // Regular line (not part of the diff)
            // If it doesn't start with - or +, treat it as context or a line to add
            if (!line.startsWith(' ')) {
                // This is a line without a prefix, treat it as an addition
                addedLines.push(line);
            }
        }
    }

    if (!silent) {
        console.log(`Found ${removedLines.length} lines to remove and ${addedLines.length} lines to add`);
    }

    // Second pass: apply the changes
    // For simplicity, we'll just replace the entire content
    // This works well for complete file replacements
    if (removedLines.length > 0 && addedLines.length > 0) {
        // Check if we're replacing the entire file
        const allLinesRemoved = originalLines.every(line =>
            removedLines.some(removedLine => removedLine.trim() === line.trim())
        );

        if (allLinesRemoved || removedLines.length >= originalLines.length * 0.8) {
            // If we're removing most or all of the file, just use the added lines
            if (!silent) {
                console.log('Replacing entire file content');
            }
            resultLines = addedLines;
        } else {
            // Otherwise, apply the changes more carefully
            if (!silent) {
                console.log('Applying changes selectively');
            }

            // Start with the original content
            resultLines = [...originalLines];

            // Remove lines
            for (const lineToRemove of removedLines) {
                const index = resultLines.findIndex(line => line.trim() === lineToRemove.trim());
                if (index !== -1) {
                    resultLines.splice(index, 1);
                    if (!silent) {
                        console.log(`Removed line: "${lineToRemove}"`);
                    }
                }
            }

            // Add lines (at the beginning for simplicity)
            // This is a simplification and might not work for all cases
            if (addedLines.length > 0) {
                resultLines = [...addedLines, ...resultLines];
                if (!silent) {
                    console.log(`Added ${addedLines.length} lines at the beginning`);
                }
            }
        }
    } else if (addedLines.length > 0) {
        // Only additions, no removals
        // In this case, we should append the additions to the original content
        resultLines = [...originalLines, ...addedLines];
        if (!silent) {
            console.log('Only additions, appending to original content');
        }
    } else if (removedLines.length > 0) {
        // Only removals, no additions
        resultLines = originalLines.filter(line =>
            !removedLines.some(removedLine => removedLine.trim() === line.trim())
        );
        if (!silent) {
            console.log('Only removals, filtering content');
        }
    } else {
        // No changes
        resultLines = originalLines;
        if (!silent) {
            console.log('No changes to apply');
        }
    }

    return resultLines.join('\n');
}
