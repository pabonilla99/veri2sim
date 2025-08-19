module selector (
  input [1:0] sel,
  input a,
  input b,
  output reg out
);

  // always @(*) begin
  always @(a, b, sel) begin
    case (sel)
      2'b00: out = a;
      2'b01: out = b;
      2'b10: out = a & b;
      2'b11: out = a | b;
      default: out = 1'b0;
    endcase
  end

endmodule