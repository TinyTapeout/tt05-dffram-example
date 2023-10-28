`default_nettype none
`timescale 1ns/1ps

/*
this testbench just instantiates the module and makes some convenient wires
that can be driven / tested by the cocotb test.py
*/

module tb (
    // testbench is controlled by test.py
    input clk,
    input rst_n,
    input ena,
    input [6:0] addr,
    input we,
    input [7:0] data_in,
    output [7:0] bidirectional_is_output,
    output [7:0] data_out
   );

    // this part dumps the trace to a vcd file that can be viewed with GTKWave
    initial begin
        $dumpfile ("tb.vcd");
        $dumpvars (0, tb);
        #1;
    end

    // instantiate the DUT
    tt_um_urish_dffram dffram(
    `ifdef GL_TEST
        .VPWR( 1'b1),
        .VGND( 1'b0),
    `endif
        .ui_in  ({we, addr}),
        .uo_out (data_out),
        .uio_in (data_in),
        .uio_oe (bidirectional_is_output),
        .ena(ena),
        .clk(clk),
        .rst_n(rst_n)
    );

endmodule