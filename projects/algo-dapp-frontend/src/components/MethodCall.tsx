import { useState } from 'react';

interface IMethodCallInterface {
  methodFunction: () => Promise<void>,
  text: string
}

let MethodCall = ({methodFunction, text}: IMethodCallInterface) => {
  let [loading, setLoading] = useState<boolean>(false);
  let callMethodFunction = async () => {
    setLoading(true);
    await methodFunction();
    setLoading(false);
  };

  return (
    <button className="btn m-2" onClick={callMethodFunction}>
      {loading ? <span className="loading loading-spinner"/> : text}
    </button>
  )
};

export default MethodCall;