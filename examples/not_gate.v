module not_gate (
    input  a,
    output b
);
    wire w;
    assign w = ~a;
    assign b = w;

endmodule
