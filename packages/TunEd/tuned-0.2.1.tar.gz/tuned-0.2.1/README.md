# TunEd

## Description

**TunEd** is a command-line tuning tool.

## Dependencies

- Python >= 3.12
- PyAudio >= 0.2.14
- sounddevice >= 0.4.6
- numpy >= 1.26.4

**TunEd** use **PyAudio** library to stream audio from your computer's microphone.

**PyAudio** need install of **PortAudio**.

- For Debian / Ubuntu Linux:

```bash
~$ apt-get install portaudio19-dev python-all-dev
```

## Installation

Using pip:

```bash
~ $ pip install tuned
```

With source:

```bash
~ $ git clone https://framagit.org/drd/tuned.git
```

Install requirements:

```bash
~ $ pip install -r requirements_dev.txt
```

To create a python package, go to inside tuned directory:

```bash
~ $ cd tuned
```

Build the package in an isolated environment, generating a source-distribution and wheel in the directory dist/ (<https://build.pypa.io/en/stable/>):

```bash
~$ python -m build
```

To install it:

```bash
~ $ pip install ./dist/tuned-0.2.1-py3-none-any.whl
```

## Usage

Launch TunEd with standard tuning frequency (@440㎐):

```bash
~$ tuned
```

To set a different tuning frequency:

```bash
~$ tuned -f 442
```

You can change the information to display:

```bash
~$ tuned -d tuner precision frequency signal_level execution_time
```

- **tuner**: Show the tuner interface.
- **precision**: Show the current value between played note and target note.
- **frequency**: Show the current note frequency.
- **signal_level**: Show the current level signal.
- **execution_time**: Show the execution time of the played note calculation.

## Authors

- **drd** - <drd.ltt000@gmail.com> - Main developper

## License

TunEd is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

TunEd is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
