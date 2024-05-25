# buildable-dataclasses
![tests](https://github.com/dertilo/buildable-dataclasses/actions/workflows/tests.yml/badge.svg)
[![pypi](https://img.shields.io/pypi/v/misc-python-utils.svg)](https://pypi.python.org/project/buildable-dataclasses)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![bear-ified](https://raw.githubusercontent.com/beartype/beartype-assets/main/badge/bear-ified.svg)](https://beartype.readthedocs.io)
[![Ruff-ified](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/dertilo/python-linters/blob/master/python_linters/ruff.toml)

batch-processing pipelines via nested dataclasses
![img.png](images/hammer.png)
### example batch-processing pipeline
- one first has to compute the dependencies before you can compute the FooBar itself
```mermaid
flowchart TD
foobar["FooBar"] --> | depends-on | dependency-a["NeededData"]
foobar["FooBar"] --> | depends-on | dependency-b["AnotherThing"]
```

### DAG declared via `Buildable`-dataclasses (foobar-example)
```python
@dataclass
class Foobar(Buildable):
    dependency_a: NeededData # another buildable dataclass
    dependency_b: AnotherThing # yet another buildable dataclass
    
    some_result: SomeDataContainer # whatever type you want

    def _build_self(self):
        self.some_result=some_fancy_processing(self.dependency_a, self.dependency_b)
    
data=Foobar(NeededData(), AnotherThing())
data.build() # first builds the dependencies then the dataclass itself (_build_self)
```
- everything is happening in memory, what about writing results to disk?

### BuildableData (foobar-example)
- writing processed data to disk (or S3/wherever)
```python
@dataclass
class FoobarData(BuildableData):
    dependency_a: NeededData
    dependency_b: AnotherThing

    @property
    def processed_data_file(self) -> str:
        return f"{self.data_dir}/processed_data.whatever"
    
    @property
    def _is_data_valid(self) -> bool:
        return Path(self.processed_data_file).is_file()

    def _build_data(self) -> None:
        processed_data=fancy_processing(self.dependency_a, self.dependency_b)
        write(self.processed_data_file, processed_data)
        
    def example_reading_method(self)->ProcessedData:
        return read(self.processed_data_file)

data=Foobar(NeededData(), AnotherThing())
data.build() #  processes data and writes it to disk
# in another python-process or another day
probably_already_processed=Foobar(NeededData(), AnotherThing())
probably_already_processed.build() # does NOT reprocess your data cause "is_data_valid" returns True
my_data=data.example_reading_method() 
```
