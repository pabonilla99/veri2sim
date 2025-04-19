module not_gate (
    input  a,
    output b
);
    wire w;  // just for test "wire" reserved word
    assign w = ~a;
    assign b = w;

endmodule
