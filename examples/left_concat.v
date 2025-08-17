module LeftConcatenation(
    input [7:0] a,  // 8-bit input
    output [3:0] b, // first 4-bit output
    output [3:0] c  // second 4-bit output
);
    // Concatenation of the two outputs
    assign {b, c} = a; // b takes the first 4 bits and c takes the last 4 bits of a
endmodule