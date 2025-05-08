# ProductMap CLI
This is a command line interface (CLI) for the ProductMap library. The CLI provides a way to interact with the library from the command line.

# Install it
Use the following command to install the library:

```bash
pip install .
```

# Usage

To use the library, you can create a script or run it directly from the command line (for local purposes):

```bash
pm-cli <file-path> <Repository-username> <Repository-email> --action=["generate", "validate"]
```

This setup provides a basic structure for validating and generating a product map. The logic for generating and validating the product map content will be added in the `validate_file` and `generate_map` functions.

# Example

Here is an example of how to use the CLI to generate a product map:

```bash
pm-cli <your-product-map-token> "tests/sample_file/main.cpp" "AxelGithub" "axel.reichwein@koneksys.com" --action="validate"
```
This command will validate the content of the `main.cpp` file and should provide an output like this:

```bash
Validating file tests/sample_file/main.cpp
File 'tests/sample_file/main.cpp' successfully read! Size: 233 bytes.
File 'tests/sample_file/main.cpp' validated successfully!
{"valid":true,"lines_of_code":6,"consumed_lines_of_code":139437,"remaining_lines_of_code":10563}
```

