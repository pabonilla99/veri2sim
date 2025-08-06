module selector_b (
  input [1:0] sel,
  input a,
  input b,
  output reg Q,
  output reg NQ
);

  // always @(*) begin
  always @(a, b, sel) begin
    case (sel)
      2'b00: begin
        Q = a;
        NQ = ~a;
      end
      2'b01: begin
        Q = b;
        NQ = ~b;
      end
      2'b10: begin
        Q = a & b;
        NQ = ~(a & b);
      end
      2'b11: begin
        Q = a | b;
        NQ = ~(a | b);
      end
      default: begin
        Q = 1'b0;
        NQ = 1'b1;
      end
    endcase
  end

endmodule