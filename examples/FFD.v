module FFD ( input D, output reg Q, input clk );
    always @(posedge clk) begin
        Q <= D;  // flip-flop behavior
    end
endmodule
