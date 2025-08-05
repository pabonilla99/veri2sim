module FFD_b ( input D, reg Q, input clk );
    always @(negedge clk) begin
        Q <= D;  // flip-flop behavior
    end
endmodule
