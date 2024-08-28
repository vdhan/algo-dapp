import * as algokit from '@algorandfoundation/algokit-utils';
import { DappClient } from './contracts/Dapp';

export function create(
  algorand: algokit.AlgorandClient,
  dmClient: DappClient,
  sender: string,
  unitaryPrice: bigint,
  quantity: bigint,
  assetBeingSold: bigint,
  setAppId: (id: number) => void
) {
  return async () => {
    let assetId = assetBeingSold;
    if (assetId === 0n) {
      let assetCreate = await algorand.send.assetCreate({sender, total: quantity});
      assetId = BigInt(assetCreate.confirmation.assetIndex!);
    }

    let createResult = await dmClient.create.createApplication({asset: assetId, unitaryPrice});
    let Txn = await algorand.transactions.payment({
      sender,
      receiver: createResult.appAddress,
      amount: algokit.algos(2),
      extraFee: algokit.algos(0.001) // fee should always 0.001
    });

    await dmClient.optInAsset({pay: Txn});
    await algorand.send.assetTransfer({assetId, sender, receiver: createResult.appAddress, amount: quantity});
    setAppId(Number(createResult.appId));
  }
}