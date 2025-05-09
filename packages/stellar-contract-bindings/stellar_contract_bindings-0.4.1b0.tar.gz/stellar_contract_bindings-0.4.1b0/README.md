# stellar-contract-bindings

`stellar-contract-bindings` is a CLI tool designed to generate language bindings for Stellar Soroban smart contracts.

This tool simplifies the process of interacting with Soroban contracts by generating the necessary code to call contract
methods directly from your preferred programming language. Currently, it supports
Python and Java. [stellar-cli](https://github.com/stellar/stellar-cli) provides support for TypeScript and Rust.

## Web Interface
We have a web interface for generating bindings. You can access via [https://stellar-contract-bindings.fly.dev/](https://stellar-contract-bindings.fly.dev/).

## Installation

You can install `stellar-contract-bindings` using pip:

```shell
pip install stellar-contract-bindings
```

## Usage

Please check the help message for the most up-to-date usage information:

```shell
stellar-contract-bindings --help
```

### Example

```shell
stellar-contract-bindings python --contract-id CDOAW6D7NXAPOCO7TFAWZNJHK62E3IYRGNRVX3VOXNKNVOXCLLPJXQCF --rpc-url https://mainnet.sorobanrpc.com --output ./bindings
```

This command will generate Python binding for the specified contract and save it in the `./bindings` directory.

### Using the Generated Binding

After generating the binding, you can use it to interact with your Soroban contract. Here's an example:

#### Python

```python
from stellar_sdk import Network
from bindings import Client  # Import the generated bindings

contract_id = "CDOAW6D7NXAPOCO7TFAWZNJHK62E3IYRGNRVX3VOXNKNVOXCLLPJXQCF"
rpc_url = "https://mainnet.sorobanrpc.com"
network_passphrase = Network.PUBLIC_NETWORK_PASSPHRASE

client = Client(contract_id, rpc_url, network_passphrase)
assembled_tx = client.hello(b"world")
print(assembled_tx.result())
# assembled_tx.sign_and_submit()
```

#### Java
```java
public class Example extends ContractClient {
    public static void main(String[] args) {
        KeyPair kp = KeyPair.fromAccountId("GD5KKP3LHUDXLDCGKP55NLEOEHMS3Z4BS6IDDZFCYU3BDXUZTBWL7JNF");
        Client client = new Client("CDOAW6D7NXAPOCO7TFAWZNJHK62E3IYRGNRVX3VOXNKNVOXCLLPJXQCF", "https://mainnet.sorobanrpc.com", Network.PUBLIC);
        AssembledTransaction<List<byte[]>> tx = client.hello("World".getBytes(), kp.getAccountId(), kp, 100);
    }
}
```

## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! The project is designed to be easy to add support for other languages, please open an issue
or submit a pull request for any improvements or bug fixes.