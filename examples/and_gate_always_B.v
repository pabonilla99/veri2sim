module and_gate_always_B (
    input  a,
    input  b,
    output c
);

    always @(a, b) begin
        c = a & b;
        c = b;
    end

endmodule
