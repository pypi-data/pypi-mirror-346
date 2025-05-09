// Import the functions we need to test
console.log("Starting test script...");
try {
    const { applyDiffToContent } = require('./utils/diff-utils');
    console.log("Successfully imported applyDiffToContent");
} catch (error) {
    console.error("Error importing from diff-utils:", error);
    process.exit(1);
}

// Test function to verify diff application
function testDiffApplication() {
    // Test 1: Standard diff with proper hunk header
    const originalContent1 = 'Line 1\nLine 2\nLine 3';
    const diff1 = '@@ -1,3 +1,3 @@\n Line 1\n-Line 2\n+Line 2 modified\n Line 3';

    console.log('Test 1: Standard diff with proper hunk header');
    console.log('Original content:', originalContent1);
    console.log('Diff:', diff1);

    const patchedContent1 = applyDiffToContent(originalContent1, diff1, true);
    console.log('Patched content:', patchedContent1);

    const expected1 = 'Line 1\nLine 2 modified\nLine 3';
    console.log('Expected content:', expected1);
    console.log('Test 1 result:', patchedContent1 === expected1 ? 'PASSED' : 'FAILED');

    // Test 2: Diff with missing line numbers in hunk header
    const originalContent2 = 'def main():\n    print("Hello, world!")\n\nif __name__ == "__main__":\n    main()';
    const diff2 = '--- app.py\n+++ app.py\n@@\n+def sample_function():\n+    print("This is a sample function for testing diffToFile.")\n';

    console.log('\nTest 2: Diff with missing line numbers in hunk header');
    console.log('Original content:', originalContent2);
    console.log('Diff:', diff2);

    const patchedContent2 = applyDiffToContent(originalContent2, diff2, true);
    console.log('Patched content:', patchedContent2);

    // The expected result should have the new function added
    const expected2 = 'def sample_function():\n    print("This is a sample function for testing diffToFile.")\ndef main():\n    print("Hello, world!")\n\nif __name__ == "__main__":\n    main()';
    console.log('Expected content:', expected2);
    console.log('Test 2 result:', patchedContent2 === expected2 ? 'PASSED' : 'FAILED');

    // Test 3: Fix the diff by adding line numbers to the hunk header
    const diff3 = '--- app.py\n+++ app.py\n@@ -1,5 +3,2 @@\n+def sample_function():\n+    print("This is a sample function for testing diffToFile.")\n';

    console.log('\nTest 3: Fixed diff with proper hunk header');
    console.log('Original content:', originalContent2);
    console.log('Diff:', diff3);

    const patchedContent3 = applyDiffToContent(originalContent2, diff3, true);
    console.log('Patched content:', patchedContent3);
    console.log('Test 3 result:', patchedContent3 === expected2 ? 'PASSED' : 'FAILED');

    // Test 4: Fibonacci example with docstring addition
    const originalContent4 = 'def print_fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        print(a)\n        a, b = b, a + b\n\n# Print the first 10 Fibonacci numbers\nprint_fibonacci(10)\n';
    const diff4 = '--- fibonacci.py\t2024-06-10 12:00:00.000000000 +0000\n+++ fibonacci.py\t2024-06-10 12:01:00.000000000 +0000\n@@ -1,6 +1,8 @@\n+"""This program prints the first n Fibonacci numbers"""\n+\ndef print_fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        print(a)\n        a, b = b, a + b\n\n# Print the first 10 Fibonacci numbers\nprint_fibonacci(10)\n';

    console.log('\nTest 4: Fibonacci example with docstring addition');
    console.log('Original content:', originalContent4);
    console.log('Diff:', diff4);

    const patchedContent4 = applyDiffToContent(originalContent4, diff4, true);
    console.log('Patched content:', patchedContent4);

    const expected4 = '"""This program prints the first n Fibonacci numbers"""\n\ndef print_fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        print(a)\n        a, b = b, a + b\n\n# Print the first 10 Fibonacci numbers\nprint_fibonacci(10)\n';
    console.log('Expected content:', expected4);
    console.log('Test 4 result:', patchedContent4 === expected4 ? 'PASSED' : 'FAILED');
}

// Run the test
testDiffApplication();
