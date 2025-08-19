module mux_2_1 (
    input sel,
    input  a,
    input  b,
    output c
);

    always @(a or b or sel) begin
        if (sel) begin
            c = b;  // If sel is high, output b
        end else begin
            c = a;  // If sel is low, output a
        end
    end

endmodule
