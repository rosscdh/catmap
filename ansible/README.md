# Chute PI


## Setup hosts

1. Edit the new-raspberry/hosts file
2. add your new host to the [raspberries] section
3. should look like:

```
[raspberries]
...
raspberry_:number ansible_ssh_host=:raspberry_ip ansible_ssh_user=pi wordpress_url=http://digitalhardcore.de/feed pusher_key=cf7fc048e21bd39e6f82 pusher_secret=01d612aade08edc9dfde
```

## Setup Authentication on the raspberries with your ssh key

will prompt you for the sudo password for the raspberry which is default: `raspberry`

```
cd new-raspberry
ansible-playbook -i hosts auth.yml  --ask-pass --sudo
```

## Update The raspberries


```
cd new-raspberry
ansible-playbook -i hosts setup.yml
```


## Installing a new release of "chute-client"


```
cp ~/chute-update-from-ross.zip new-raspberry/roles/chute-client/files/chute-client.zip
```

### If you have access to thte chute-client reporsitory

```
cd chute-client
make release
```

The **make release** command copies the created zip to 1 level above the chute-client ie. '../ansible-raspberry-pi/new-raspberry/roles/chute-client/files/chute-client.zip'