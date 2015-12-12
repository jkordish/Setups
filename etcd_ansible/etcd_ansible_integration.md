title: etcd + ansible = crazy delicious
date: 2014-03-16

# Overview

[Ansible](https://github.com/ansible/ansible) is an amazingly simple but extremely powerful system automation tool akin to Chef and Puppet.
[etcd](https://github.com/coreos/etcd/) is a highly scalable key/value store written in Go that uses [raft](http://raftconsensus.github.io/) for consensus.

The reason I looked at something like etcd in our ansible automation process is *flat files are difficult to scale*. This was a problem that we ran into as in our deployments we had customer specific environments. This meant customer specific host files, customer specific var files, etc. Managing those files became tedious and created unneeded friction in the deployment process. The goal then became to centrally manage customer specific environments in a programmatic implementation.

**note: I will not cover how to install either etcd nor ansible**
**note: I'm using a single etcd install on the local host for examples**

## Reason

The reason etcd was chosen was due to the simplicity in its installation, configuration and management. It also provided the following benefits:
  * rest api (curl or [etcdctl](https://github.com/coreos/etcdctl))
  * secure access (certs)
  * highly distributed and fault tolerant (via [raft](http://raftconsensus.github.io/))
  * version control (POST to directories)
  * Backups (easily dump key/value to flat file [etcd-dump](https://www.npmjs.org/package/etcd-dump))

Etcd felt very much like Ansible as it did not try to solve all problems for you but rather enable you to build your own solution.

## Integration

Initial integration between etcd and Ansible attempted to solve the two basic problems:
  * customer host file
  * customer var file

The biggest challenge in the process was actually converting both to json style formats that Ansible could understand.

### Structure

The structure hierarchy of the etcd became as follows:
    customers/customer_id/hosts
    customers/customer_id/vars

With both hosts and vars being directories. Allowing both vars and hosts to be directories and POST'ing data to it you actually ended up with something like:
    customers/customer_id/hosts/124
    customers/customer_id/hosts/130
    customers/customer_id/hosts/143

Each incremented key being a newer value of the customer's host file. The vars would look similar which incremented key with the latest value. This provided version control as you are then able to compare values and then just remove the offending key to roll back. Simple.

### Host file

Storing the customer hosts file then was a matter of converting the Ansible ini formatted file to json. Example: **[hosts.json](https://raw.githubusercontent.com/joethemongoose/Setups/master/etcd_ansible/hosts.json)**

Once formatted you then just POST the json file into the customer hosts directory with curl.

    curl -L http://127.0.0.1:4001/v2/keys/customers/xyz/hosts -XPOST --data-urlencode value@hosts.json

Ansible can then utilize a [dynamic inventory](http://docs.ansible.com/intro_dynamic_inventory.html) for gathering the host inventory file. What you then need here is a python scrip that can query etcd and output that host inventory. Ansible will execute a python script by attempting to pass --list to it so your python script must adhere to that. More documentation can be found [here](http://docs.ansible.com/developing_inventory.html)

Here is an example of a [hosts.py](https://raw.githubusercontent.com/joethemongoose/Setups/master/etcd_ansible/hosts.py) script that when executed with --list argument will walk down the etcd structure and get the most recent key. All that is then needed is changing your ansible.cfg to read:

    hostfile       = /path_to_file/hosts.py

If you notice I have it reading a environmental variable of ANSIBLE_ID which would actually correlate to the customer id. So executing it could be done by exporting that environmental variable prior to run or even:

    ANSIBLE_ID=zyx ansible-playbook deploy.yml

### Var file

Very similar to the host configuration of a json formatted key/value and a assistant python script we also can do the same for the customer var file.

Of course one would need to format their var file in json. Example:**[vars.json](https://raw.githubusercontent.com/joethemongoose/Setups/master/etcd_ansible/vars.json)**

Then one would just POST that to the customer vars directory:

    curl -L http://127.0.0.1:4001/v2/keys/customers/xyz/vars -XPOST --data-urlencode value@vars.json

Then a quick python script, [vars.py](https://raw.githubusercontent.com/joethemongoose/Setups/master/etcd_ansible/vars.py), can be created to get the latest key/value pair for use in Ansible.

Tying the hosts.py and the vars.py becomes a matter of just:

    ANSIBLE_ID=zyx ansible-playbook -e "$(vars.py)" deploy.yml

## Post Integration

After the first problems were solved it became apparent that etcd could do much more than providing a convenient key/value store for hosts and vars.

  * populating customer specific users in the mongodb backend
  * collecting installed application versions and POST'ing to etcd

This can be accomplished by using registering values from a command on the host and then using a local_action to POST to etcd.

In roles/collect_version/tasks/main.yml

    - name: copy version upload python script
      action: copy src=enum-versions.py dest=/usr/local/bin/enum-versions.py mode=0755 owner=root group=root
    
    - name: execute enumurate version script
      action: command /usr/local/bin/enum-versions.py
      register: versions
      notify: send to etcd

In roles/collect_version/handlers/main.yml

    - name: send to etcd
      local_action: command {{item}}
      with_items:
      - ‘curl -L http://127.0.0.1:4001/v2/keys/customers/{{id}}/version/{{name}} -XPUT -d dir=true’
      - ‘curl -L http://127.0.0.1:4001/v2/keys/customers/{{id}}/version/{{name}} -XPOST -d value=“{{ versions.stdout }}”’

Likewise we can query etcd using a local_action, register values, and then walk through those values against the host. In this example I can get json formatted users from etcd and then using a local python script on the box send each to the mongodb instance.

In roles/mongodb/tasks/main.yml

    - name: Get Users
      local_action: command users.py
      register: users
    
    - name: Add Users
      action: command python add_user.py '{{item}}'
      with_items: users.stdout_lines

### footnote
Questions/Comments/Priases can be sent to me at <joe@unicornclouds.com>
