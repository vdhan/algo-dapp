from algopy import ARC4Contract, Asset, Global, Txn, UInt64, gtxn, itxn
from algopy.arc4 import abimethod


class Dapp(ARC4Contract):
    asset_id: UInt64
    unitary_price: UInt64

    @abimethod(create='require', allow_actions=['NoOp'])
    def create_application(self, asset: Asset, unitary_price: UInt64) -> None:
        self.asset_id = asset.id
        self.unitary_price = unitary_price

    @abimethod
    def opt_in_asset(self, pay: gtxn.PaymentTransaction) -> None:
        assert Txn.sender == Global.creator_address
        assert not Global.current_application_address.is_opted_in(Asset(self.asset_id))
        assert pay.receiver == Global.current_application_address
        assert pay.amount == Global.min_balance + Global.asset_opt_in_min_balance

        itxn.AssetTransfer(
            xfer_asset=self.asset_id, asset_receiver=Global.current_application_address, asset_amount=0).submit()

    @abimethod
    def set_price(self, unitary_price: UInt64) -> None:
        assert Txn.sender == Global.creator_address
        self.unitary_price = unitary_price

    @abimethod
    def buy(self, pay: gtxn.PaymentTransaction, quantity: UInt64) -> None:
        assert self.unitary_price != 0
        assert pay.sender == Txn.sender
        assert pay.receiver == Global.current_application_address
        assert pay.amount == quantity * self.unitary_price

        itxn.AssetTransfer(xfer_asset=self.asset_id, asset_receiver=Txn.sender, asset_amount=quantity).submit()

    @abimethod(allow_actions=['DeleteApplication'])
    def delete_application(self) -> None:
        assert Txn.sender == Global.creator_address
        itxn.AssetTransfer(
            xfer_asset=self.asset_id, asset_receiver=Global.creator_address, asset_amount=0,
            asset_close_to=Global.creator_address).submit()

        itxn.Payment(receiver=Global.creator_address, amount=0, close_remainder_to=Global.creator_address).submit()
