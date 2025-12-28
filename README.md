```
# Hetzner cloud + Terraform (Ubuntu 22.04 server with docker & ollama) 
# Docker compose and workflows create web page with Deepseek model (deepseek-coder:6.7b)
```
### Terraform: create server
### Cloud-init: prepare Ollama + Custom Model.
### Docker Compose: put together Nginx, Python and Cloudflare.
### GitHub Actions: automates code updates via SSH tunnel.
```
### 1. Create file terraform.tfvars and add 
```

```
hcloud_token = "YourToken"
ssh_user = "YourUser"
ssh_public_key = "~/.ssh/id_rsa.pub"
cloudflare_token = "YourTocken"
```

```
### If You need edit cloud-init file.
```

```
### Terraform commands:
### terraform init
### terraform plan
### terraform apply
```

```
### Test cloud init
### cloud-init status --long
```

```
### Add github key
### cd ~/.ssh
### cat github_actions.pub >> authorized_keys
### github_actions.pub: command not found
### chmod 600 authorized_keys
```

```
## Manual install if don't use Terraform...
### curl -fsSL https://ollama.com/install.sh | sh
### ollama --version
### python main file "model": "deepseek-custom" because cloud init use: 
cat <<EOF > /home/${ssh_user}/Modelfile
    FROM deepseek-coder:6.7b
    PARAMETER num_ctx 4096
    PARAMETER num_thread 4
    EOF
### ollama pull deepseek-coder:6.7b
### /var/lib/ollama/
### ollama run deepseek-coder:6.7b
### sudo systemctl enable ollama
### sudo systemctl start ollama
```

```
Github need add secrets for workflow:
TEST_SERVER_SSH_PRIVATE_KEY
TEST_SERVER_USER
TEST_SERVER_IP
TEST_TUNNEL_TOKEN - from your cloudflare
```

```
Edit nginx.conf, because I have cloudflare Flexible
```