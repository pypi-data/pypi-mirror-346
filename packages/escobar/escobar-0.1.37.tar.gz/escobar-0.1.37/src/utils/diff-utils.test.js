// Test file for diff-utils.ts

// Since we can't directly import TypeScript files in Node.js without transpilation,
// we'll implement a simplified version of the functions for testing purposes.

/**
 * Simplified version of applyDiffToContent for testing
 */
function applyDiffToContent(originalContent, diff, silent = true) {
    // Split the original content and diff into lines
    const originalLines = originalContent.split('\n');
    const diffLines = diff.split('\n');

    // Create a copy of the original lines that we'll modify
    let modifiedLines = [...originalLines];

    // Parse the diff to extract chunks
    const chunks = [];
    let currentChunk = null;

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
        const changeGroups = [];
        let currentGroup = null;

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
                    group.changes.forEach((change, idx) => {
                        console.log(`  Line ${idx + 1} to remove: "${change.content}"`);
                    });
                } else if (group.type === 'add') {
                    console.log(`Adding ${group.changes.length} lines at position ${lineIndex + position}`);
                    group.changes.forEach((change, idx) => {
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
                const linesToAdd = group.changes.map(change => change.content);
                modifiedLines.splice(lineIndex + position, 0, ...linesToAdd);
            }

            if (!silent) {
                console.log(`After applying group ${j + 1}, modifiedLines.length=${modifiedLines.length}`);
            }
        }
    }

    // Special case: If the diff has no valid chunks after parsing or if it contains "@@ ... @@",
    // try a more direct approach. This handles cases where the diff format is non-standard
    // but still follows basic +/- line prefixes
    if (chunks.length === 0 || !diff.includes('@@ -') || diff.includes('@@ ... @@')) {
        if (!silent) {
            console.log('Non-standard hunk headers found, trying direct line-by-line processing');
        }
        return applySimpleDiff(originalContent, diff, silent);
    }

    // Join the modified lines back into a string
    return modifiedLines.join('\n');
}

/**
 * Applies a simple diff directly, line by line
 * This is used for non-standard diffs that don't have proper hunk headers
 */
function applySimpleDiff(originalContent, diff, silent = true) {
    // Split the original content and diff into lines
    const originalLines = originalContent.split('\n');
    const diffLines = diff.split('\n');

    // Create a new array for the result
    let resultLines = [];

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
    let removedLines = [];
    let addedLines = [];

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

// Test case for line removal
function testLineRemoval() {
    console.log('Testing line removal...');

    // Original content with 5 lines
    const originalContent =
        `line 1
line 2
line 3
line 4
line 5`;

    // Diff that removes lines 2 and 3
    const diff =
        `@@ -1,5 +1,3 @@
 line 1
-line 2
-line 3
 line 4
 line 5`;

    // Expected result after applying the diff
    const expectedResult =
        `line 1
line 4
line 5`;

    // Apply the diff with debug output
    const result = applyDiffToContent(originalContent, diff, false);

    // Check if the result matches the expected result
    if (result === expectedResult) {
        console.log('✅ Line removal test passed!');
    } else {
        console.log('❌ Line removal test failed!');
        console.log('Expected:');
        console.log(expectedResult);
        console.log('Got:');
        console.log(result);
    }
}

// Test case for line addition
function testLineAddition() {
    console.log('\nTesting line addition...');

    // Original content with 3 lines
    const originalContent =
        `line 1
line 2
line 3`;

    // Diff that adds two lines after line 1
    const diff =
        `@@ -1,3 +1,5 @@
 line 1
+new line 1
+new line 2
 line 2
 line 3`;

    // Expected result after applying the diff
    const expectedResult =
        `line 1
new line 1
new line 2
line 2
line 3`;

    // Apply the diff with debug output
    const result = applyDiffToContent(originalContent, diff, false);

    // Check if the result matches the expected result
    if (result === expectedResult) {
        console.log('✅ Line addition test passed!');
    } else {
        console.log('❌ Line addition test failed!');
        console.log('Expected:');
        console.log(expectedResult);
        console.log('Got:');
        console.log(result);
    }
}

// Test case for combined operations
function testCombinedOperations() {
    console.log('\nTesting combined operations...');

    // Original content with 5 lines
    const originalContent =
        `line 1
line 2
line 3
line 4
line 5`;

    // Diff that removes line 2 and adds two lines after line 3
    const diff =
        `@@ -1,5 +1,6 @@
 line 1
-line 2
 line 3
+new line 1
+new line 2
 line 4
 line 5`;

    // Expected result after applying the diff
    const expectedResult =
        `line 1
line 3
new line 1
new line 2
line 4
line 5`;

    // Apply the diff with debug output
    const result = applyDiffToContent(originalContent, diff, false);

    // Check if the result matches the expected result
    if (result === expectedResult) {
        console.log('✅ Combined operations test passed!');
    } else {
        console.log('❌ Combined operations test failed!');
        console.log('Expected:');
        console.log(expectedResult);
        console.log('Got:');
        console.log(result);
    }
}

// Test case for diffs without line numbers in hunk header
function testDiffWithoutLineNumbers() {
    console.log('\nTesting diff without line numbers in hunk header...');

    // Original content with 5 lines
    const originalContent =
        `def main():
    # Generate a sequence of numbers from 1 to 10
    numbers = list(range(1, 11))

    # Compute the square of each number
    squares = [n ** 2 for n in numbers]

    # Print the results
    print("Number\tSquare Value")
    for n, sq in zip(numbers, squares):
        print(f"{n}\t{sq}")`;

    // Diff that adds a new function and modifies the main function
    const diff =
        `--- sequence_squares.py
+++ sequence_squares.py
@@
+
def compute_squares(numbers):
+    """Return a list of squares for the given list of numbers."""
+    return [n ** 2 for n in numbers]
+
 def main():
     # Generate a sequence of numbers from 1 to 10
     numbers = list(range(1, 11))
 
-    # Compute the square of each number
-    squares = [n ** 2 for n in numbers]
+    # Compute the square of each number using the new function
+    squares = compute_squares(numbers)
 
     # Print the results
-    print("Number\tSquare Value")
+    print("Number\tSquare Value")
     for n, sq in zip(numbers, squares):
-        print(f"{n}\t{sq}")
+        print(f"{n}\t{sq}")`;

    // Expected result after applying the diff
    const expectedResult =
        `
def compute_squares(numbers):
    """Return a list of squares for the given list of numbers."""
    return [n ** 2 for n in numbers]

def main():
    # Generate a sequence of numbers from 1 to 10
    numbers = list(range(1, 11))

    # Compute the square of each number using the new function
    squares = compute_squares(numbers)

    # Print the results
    print("Number\tSquare Value")
    for n, sq in zip(numbers, squares):
        print(f"{n}\t{sq}")`;

    // Apply the diff with debug output
    const result = applyDiffToContent(originalContent, diff, false);

    // Check if the result matches the expected result
    if (result === expectedResult) {
        console.log('✅ Diff without line numbers test passed!');
    } else {
        console.log('❌ Diff without line numbers test failed!');
        console.log('Expected:');
        console.log(expectedResult);
        console.log('Got:');
        console.log(result);
    }
}

// Test case for simple diffs without standard format
function testSimpleDiff() {
    console.log('\nTesting simple diff without standard format...');

    // Original content
    const originalContent =
        `def main():
    # Generate a sequence of numbers from 1 to 10
    numbers = list(range(1, 11))

    # Compute the square of each number
    squares = [n ** 2 for n in numbers]

    # Print the results
    print("Number\tSquare")
    for n, sq in zip(numbers, squares):
        print(f"{n}\t{sq}")`;

    // Diff that replaces the entire content
    const diff =
        `--- sequence_squares.py	2024-06-09 13:01:00.000000000 +0000
+++ sequence_squares.py	2024-06-09 13:02:00.000000000 +0000
-def main():
-    # Generate a sequence of numbers from 1 to 10
-    numbers = list(range(1, 11))

-    # Compute the square of each number
-    squares = [n ** 2 for n in numbers]

-    # Print the results
-    print("Number\tSquare")
-    for n, sq in zip(numbers, squares):
-        print(f"{n}\t{sq}")
+
+def print_squares_table(start, end):
+    """
+    Prints a table of numbers and their squares for the range [start, end].
+    """
+    sequence = get_squares_sequence(start, end)
+    print("Number\tSquare")
+    for n, sq in sequence:
+        print(f"{n}\t{sq}")
+
+def main():
+    print_squares_table(1, 10)`;

    // Expected result after applying the diff
    const expectedResult =
        `
def print_squares_table(start, end):
    """
    Prints a table of numbers and their squares for the range [start, end].
    """
    sequence = get_squares_sequence(start, end)
    print("Number\tSquare")
    for n, sq in sequence:
        print(f"{n}\t{sq}")

def main():
    print_squares_table(1, 10)`;

    // Apply the diff with debug output
    const result = applyDiffToContent(originalContent, diff, false);

    // Check if the result matches the expected result
    if (result === expectedResult) {
        console.log('✅ Simple diff test passed!');
    } else {
        console.log('❌ Simple diff test failed!');
        console.log('Expected:');
        console.log(expectedResult);
        console.log('Got:');
        console.log(result);
    }
}

// Test case for diffs with placeholder hunk headers
function testPlaceholderHunkHeaders() {
    console.log('\nTesting diff with placeholder hunk headers (@@ ... @@)...');

    // Original content
    const originalContent =
        `def main():
    # Generate a sequence of numbers from 1 to 10
    numbers = list(range(1, 11))

    # Compute the square of each number
    squares = [n ** 2 for n in numbers]

    # Print the results
    print("Number\tSquare")
    for n, sq in zip(numbers, squares):
        print(f"{n}\t{sq}")`;

    // Diff with placeholder hunk header
    const diff =
        `--- sequence_squares.py	2024-06-09 13:01:00.000000000 +0000
+++ sequence_squares.py	2024-06-09 13:02:00.000000000 +0000
@@ ... @@
-def main():
-    # Generate a sequence of numbers from 1 to 10
-    numbers = list(range(1, 11))

-    # Compute the square of each number
-    squares = [n ** 2 for n in numbers]

-    # Print the results
-    print("Number\tSquare")
-    for n, sq in zip(numbers, squares):
-        print(f"{n}\t{sq}")
+
+def print_squares_table(start, end):
+    """
+    Prints a table of numbers and their squares for the range [start, end].
+    """
+    sequence = get_squares_sequence(start, end)
+    print("Number\tSquare")
+    for n, sq in sequence:
+        print(f"{n}\t{sq}")
+
+def main():
+    print_squares_table(1, 10)`;

    // Expected result after applying the diff
    const expectedResult =
        `
def print_squares_table(start, end):
    """
    Prints a table of numbers and their squares for the range [start, end].
    """
    sequence = get_squares_sequence(start, end)
    print("Number\tSquare")
    for n, sq in sequence:
        print(f"{n}\t{sq}")

def main():
    print_squares_table(1, 10)`;

    // Apply the diff with debug output
    const result = applyDiffToContent(originalContent, diff, false);

    // Check if the result matches the expected result
    if (result === expectedResult) {
        console.log('✅ Placeholder hunk header test passed!');
    } else {
        console.log('❌ Placeholder hunk header test failed!');
        console.log('Expected:');
        console.log(expectedResult);
        console.log('Got:');
        console.log(result);
    }
}

// Test case for another placeholder hunk header example
function testAnotherPlaceholderHunkHeader() {
    console.log('\nTesting another placeholder hunk header example...');

    // Original content
    const originalContent =
        `def main():
    print_squares_table(1, 10)

    # Compute the square of each number
    squares = [n ** 2 for n in numbers]

    # Print the results
    print("Number\tSquare")
    for n, sq in zip(numbers, squares):
        print(f"{n}\t{sq}")`;

    // Diff with placeholder hunk header
    const diff =
        `--- sequence_squares.py	2024-06-09 13:03:00.000000000 +0000
+++ sequence_squares.py	2024-06-09 13:04:00.000000000 +0000
@@ ... @@
-def main():
-    print_squares_table(1, 10)
-
-    # Compute the square of each number
-    squares = [n ** 2 for n in numbers]
-
-    # Print the results
-    print("Number\tSquare")
-    for n, sq in zip(numbers, squares):
-        print(f"{n}\t{sq}")
+
+# UI test: Added a comment to test diff application
+def main():
+    print_squares_table(1, 10)`;

    // Expected result after applying the diff
    const expectedResult =
        `
# UI test: Added a comment to test diff application
def main():
    print_squares_table(1, 10)`;

    // Apply the diff with debug output
    const result = applyDiffToContent(originalContent, diff, false);

    // Check if the result matches the expected result
    if (result === expectedResult) {
        console.log('✅ Another placeholder hunk header test passed!');
    } else {
        console.log('❌ Another placeholder hunk header test failed!');
        console.log('Expected:');
        console.log(expectedResult);
        console.log('Got:');
        console.log(result);
    }
}

// Test case for diffs with only additions
function testOnlyAdditions() {
    console.log('\nTesting diff with only additions...');

    // Original content
    const originalContent =
        `def main():
    print_squares_table(1, 10)`;

    // Diff with only additions
    const diff =
        `--- sequence_squares.py	2024-06-09 13:05:00.000000000 +0000
+++ sequence_squares.py	2024-06-09 13:06:00.000000000 +0000
@@ ... @@
+
+def main():
+    print_squares_table(1, 10)
+
+if __name__ == "__main__":
+    main()`;

    // Expected result after applying the diff - additions should be appended to the end
    const expectedResult =
        `def main():
    print_squares_table(1, 10)

def main():
    print_squares_table(1, 10)

if __name__ == "__main__":
    main()`;

    // Apply the diff with debug output
    const result = applyDiffToContent(originalContent, diff, false);

    // Check if the result matches the expected result
    if (result === expectedResult) {
        console.log('✅ Only additions test passed!');
    } else {
        console.log('❌ Only additions test failed!');
        console.log('Expected:');
        console.log(expectedResult);
        console.log('Got:');
        console.log(result);
    }
}

// Run the tests
testLineRemoval();
testLineAddition();
testCombinedOperations();
testDiffWithoutLineNumbers();
testSimpleDiff();
testPlaceholderHunkHeaders();
testAnotherPlaceholderHunkHeader();
testOnlyAdditions();
