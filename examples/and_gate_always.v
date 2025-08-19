module and_gate_always (
    input  a,
    input  b,
    output c
);

    always @(a or b) begin
        c = a & b;
        c = b;
    end

endmodule
