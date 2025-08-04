module mux_2_1_B (
    input sel,
    input  a,
    input  b,
    output c
);

    always @(a or b or sel) begin
        if (sel)
            c = b;  // If sel is high, output b
        else
            c = a;  // If sel is low, output a
    end

endmodule
