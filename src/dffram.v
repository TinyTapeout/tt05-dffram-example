// SPDX-FileCopyrightText: © 2023 Uri Shaked <uri@wokwi.com>
// SPDX-License-Identifier: Apache

`define default_netname none

/* verilator lint_off UNUSEDSIGNAL */

module tt_um_urish_dffram (
`ifdef USE_POWER_PINS
  input VPWR,
  input VGND,
`endif
  input  wire [7:0] ui_in,   // Dedicated inputs
  output wire [7:0] uo_out,  // Dedicated outputs
  input  wire [7:0] uio_in,  // IOs: Input path
  output wire [7:0] uio_out, // IOs: Output path
  output wire [7:0] uio_oe,  // IOs: Enable path (active high: 0=input, 1=output)
  input  wire       ena,
  input  wire       clk,
  input  wire       rst_n
);

  wire [6:0] addr = ui_in[6:0];
  wire [1:0] byte_index = addr[1:0];
  
  assign uio_oe = 8'b0; // All bidirectional IOs are inputs
  assign uio_out = 8'b0;
  
  wire WE = ui_in[7];
  wire WE0 = WE && (byte_index == 0);
  wire WE1 = WE && (byte_index == 1);
  wire WE2 = WE && (byte_index == 2);
  wire WE3 = WE && (byte_index == 3);

  wire [4:0] bit_index = {byte_index, 3'b000};
  wire [31:0] Di0 = {24'b0, uio_in} << bit_index;
  wire [31:0] Do0;
  reg  [4:0] out_bit_index;
  assign uo_out = Do0[out_bit_index +: 8];

  RAM32 ram1 (
  `ifdef USE_POWER_PINS
    .VPWR(VPWR),
    .VGND(VGND),
  `endif
    .CLK(clk),
    .EN0(rst_n),
    .A0(addr[6:2]),
    .WE0({WE3, WE2, WE1, WE0}),
    .Di0(Di0),
    .Do0(Do0)
  );

  always @(posedge clk)
  begin
    if(rst_n) begin
      out_bit_index <= bit_index;
    end else 
      out_bit_index <= 0;
  end

endmodule
