# Valdar

Python package for radar data validation.

## Example

```python
from valdar import RadarAnalyzer

analyzer = RadarAnalyzer("/path/to/pext")
report = analyzer.evaluate()

print(report.lrr_status)
print(report.valid_lrr)
```
