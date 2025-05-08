#
# MIT License
#
# Copyright (c) 2024-2025 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Test Importer."""

import ucdp as u

import ucdpsv as usv


class TopMod(u.AMod):
    """Example Module."""

    filelists: u.ClassVar[u.ModFileLists] = (u.ModFileList(name="hdl", filepaths=("testdata/importer/top.sv",)),)

    def _build(self) -> None:
        usv.import_params_ports(self)


def test_verilog2ports():
    """Test verilog2ports."""
    top = TopMod()
    assert tuple(top.params) == (
        u.Param(u.IntegerType(), "param_p"),
        u.Param(u.IntegerType(), "width_p"),
        u.Param(u.UintType(u.Param(u.IntegerType(), "param_p")), "default_p"),
    )
    assert tuple(repr(port) for port in top.ports) == (
        "Port(BitType(), 'main_clk_i', direction=IN)",
        "Port(BitType(), 'main_rst_an_i', direction=IN)",
        "Port(BitType(), 'intf_rx_o', direction=OUT)",
        "Port(BitType(), 'intf_tx_i', direction=IN)",
        "Port(UintType(2), 'bus_trans_i', direction=IN)",
        "Port(UintType(32), 'bus_addr_i', direction=IN)",
        "Port(BitType(), 'bus_write_i', direction=IN)",
        "Port(UintType(32), 'bus_wdata_i', direction=IN)",
        "Port(BitType(), 'bus_ready_o', direction=OUT)",
        "Port(BitType(), 'bus_resp_o', direction=OUT)",
        "Port(UintType(32), 'bus_rdata_o', direction=OUT)",
        "Port(UintType(9), 'brick_o', direction=OUT, ifdef='ASIC')",
        "Port(UintType(Param(IntegerType(), 'param_p')), 'data_i', direction=IN)",
        "Port(UintType(Param(IntegerType(), 'width_p')), 'cnt_o', direction=OUT)",
        "Port(BitType(), 'key_valid_i', direction=IN)",
        "Port(BitType(), 'key_accept', direction=OUT)",
        "Port(UintType(9), 'key_data', direction=IN)",
        "Port(UintType(4), 'bidir', direction=INOUT)",
        "Port(UintType(9), 'value_o', direction=OUT, ifdef='ASIC')",
    )


class OtherMod(u.AMod):
    """Example Module."""

    filelists: u.ClassVar[u.ModFileLists] = (u.ModFileList(name="hdl", filepaths=("testdata/importer/top.sv",)),)

    def _build(self) -> None:
        usv.import_params_ports(
            self,
            portattrs={
                "main_clk_i": {"type_": u.ClkType()},
                "in*_tx_i": {"type_": u.BitType(default=1), "comment": "a comment"},
            },
        )


def test_verilog2ports_attrs():
    """Test verilog2ports."""
    top = OtherMod()
    assert tuple(top.params) == (
        u.Param(u.IntegerType(), "param_p"),
        u.Param(u.IntegerType(), "width_p"),
        u.Param(u.UintType(u.Param(u.IntegerType(), "param_p")), "default_p"),
    )
    assert tuple(repr(port) for port in top.ports) == (
        "Port(ClkType(), 'main_clk_i', direction=IN, doc=Doc(title='Clock'))",
        "Port(BitType(), 'main_rst_an_i', direction=IN)",
        "Port(BitType(), 'intf_rx_o', direction=OUT)",
        "Port(BitType(default=1), 'intf_tx_i', direction=IN, doc=Doc(comment='a comment'))",
        "Port(UintType(2), 'bus_trans_i', direction=IN)",
        "Port(UintType(32), 'bus_addr_i', direction=IN)",
        "Port(BitType(), 'bus_write_i', direction=IN)",
        "Port(UintType(32), 'bus_wdata_i', direction=IN)",
        "Port(BitType(), 'bus_ready_o', direction=OUT)",
        "Port(BitType(), 'bus_resp_o', direction=OUT)",
        "Port(UintType(32), 'bus_rdata_o', direction=OUT)",
        "Port(UintType(9), 'brick_o', direction=OUT, ifdef='ASIC')",
        "Port(UintType(Param(IntegerType(), 'param_p')), 'data_i', direction=IN)",
        "Port(UintType(Param(IntegerType(), 'width_p')), 'cnt_o', direction=OUT)",
        "Port(BitType(), 'key_valid_i', direction=IN)",
        "Port(BitType(), 'key_accept', direction=OUT)",
        "Port(UintType(9), 'key_data', direction=IN)",
        "Port(UintType(4), 'bidir', direction=INOUT)",
        "Port(UintType(9), 'value_o', direction=OUT, ifdef='ASIC')",
    )
