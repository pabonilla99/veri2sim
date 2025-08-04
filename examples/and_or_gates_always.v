module and_gate_always (
    input  a,
    input  b,
    output c,
    output d
);

    always @(a or b) begin
        c = a & b;  // AND operation
        d = a | b;  // OR operation
    end

endmodule