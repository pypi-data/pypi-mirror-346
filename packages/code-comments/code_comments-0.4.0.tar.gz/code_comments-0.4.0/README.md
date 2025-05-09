# code-comments

This project was created as a way of creating a central "annotation" file of all the useful
notes that might be created in a code base such as `todo` or `trivy` comments.

## Configuration

The project can be configured via a TOML file which by default is called `.code-annotations.toml` but can be override with the `--config` flag.

Below is an example which can be found at `.code-annotations.toml`

```TOML
file_suffix=[".tf"]
output_file="ANNOTATIONS.md"
comment_syntax = ["#"]

[[headers]]
comment = "tfsec"
table_headers = "File:Line|Type|Comment"
[[headers]]
comment = "todo"
table_headers = "File:Line|Date|Comment"

```
