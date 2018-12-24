# tue-env
Package manager that can be used to install (ROS) dependencies

## Installation

#### Ubuntu 16.04
```bash
source <(wget -O- https://raw.githubusercontent.com/tue-robotics/tue-env/master/installer/scripts/bootstrap-ros-kinetic)
tue-get install tue-dev #or
tue-get install tue-dev-full #tue-dev plus extra tools
source ~/.bashrc
```

## Usage

With `tue-get` you can install various targets which mostly are ros packages. 
The list of packages can be seen [here](installer/targets).

```bash
tue-get install <TARGET_NAME>
```
For example, so install a default developement installation for working with 
TU/e robots, run the following command:
```bash
tue-get install tue-dev
```
So automatically source the installer and corresponding workspaces run the following
command in a shell.
```bash
echo -e "export TUE_ENV=$TUE_ENV\nsource ~/.tue/setup.bash" >> ~/.bashrc
```

## Create a new target
A target can consist of the following three files:
1. `install.yaml`
2. `install.bash`
3. `setup`

Installation happens in the above order. First `install.yaml` is parsed and the
instructions in it are executed. Then `install.bash` is executed. This must have
commands/instructions that cannot be specified in the YAML file. Lastly, the
`setup` file is sourced in the bash environment by `setup.bash` of tue-env.

### Naming conventions
Name of the target must start with `ros-` only if it will be compiled/installed by ROS or it is installed by reading the dependencies from a catkin `package.xml`

### Writing `install.yaml`
| Symbol | Convention                             |
|--------|----------------------------------------|
| []     | Alternate options                      |
| <>     | Input argument required with the field |

Some fields are mentioned to be optional.

Taking the above into account, the following combinations for `install.yaml` are possible:

#### ROS package install
1. From source
```yaml
- type: ros
  source:
    type: git [svn]
    url: <Repository URL>
    sub-dir: <Sub directory of the repository> (Optional field)
    version: <Version to be installed> (Optional field)
```
2. From system
```yaml
- type: ros
  source:
    type: system
    name: <Package name>
```

#### Target / System / PIP / PPA / Snap
```yaml
- type: [target/system/pip/ppa/snap]
  name: <Name of the candidate>
```


