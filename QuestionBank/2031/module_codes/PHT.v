/*
PHT [14M]: Marking scheme: Initialization { Incomplete initialization - 0M Correct initialization - 4M}, PHT_table counter update logic and reset values {Arbitary code - 0, Partially correct code - 5M, Completely correct - 10M}
*/
// -----------------------------
// PHT module (combinational read, synchronous update)
// -----------------------------
module PHT (
    input  wire        clk,
    input  wire        reset,
    input  wire        update_en,
    input  wire [2:0]  index,
    input  wire        actual,
    output reg  [1:0]  pht_out
);
    reg [1:0] pht_array [0:7];
    integer i;

    // Combinational read (pre-update view)
    always @(*) begin
        pht_out = pht_array[index];
    end

    // Synchronous reset + update
    always @(posedge clk) begin
        if (reset) begin
            for (i = 0; i < 8; i = i + 1)
                pht_array[i] <= 2'b10;  // Weakly Taken
        end else if (update_en) begin
            if (actual) begin
                if (pht_array[index] != 2'b11)
                    pht_array[index] <= pht_array[index] + 1'b1;
            end else begin
                if (pht_array[index] != 2'b00)
                    pht_array[index] <= pht_array[index] - 1'b1;
            end
        end
    end
endmodule