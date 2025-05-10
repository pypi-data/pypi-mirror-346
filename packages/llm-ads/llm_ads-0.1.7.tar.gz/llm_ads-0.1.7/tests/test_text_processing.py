import pytest
from backend.llm_ads.utils import (
    detect_format_type,
    segment_response,
    segment_markup,
    is_factual_response
)

class TestFormatDetection:
    """Tests for the format detection functionality."""
    
    def test_detect_plain_text(self):
        """Test that plain text is correctly detected."""
        content = "This is a simple plain text response with no special formatting."
        assert detect_format_type(content) == "plain"
        
    def test_detect_markdown(self):
        """Test that markdown is correctly detected."""
        content = """# Heading
        
This is a markdown *formatted* text with **bold** and _italic_ elements.

## Subheading

- List item 1
- List item 2

```python
print("Code block")
```
        """
        assert detect_format_type(content) == "markdown"
        
    def test_detect_html(self):
        """Test that HTML is correctly detected."""
        content = """<html>
<head>
    <title>Test</title>
</head>
<body>
    <h1>Heading</h1>
    <p>This is an HTML response.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</body>
</html>
        """
        assert detect_format_type(content) == "html"
        
    def test_detect_json(self):
        """Test that JSON is correctly detected."""
        content = """
{
    "name": "John",
    "age": 30,
    "city": "New York",
    "items": ["item1", "item2", "item3"],
    "nested": {
        "key": "value"
    }
}
        """
        assert detect_format_type(content) == "json"
        
    def test_detect_code(self):
        """Test that code is correctly detected."""
        content = """
def hello_world():
    print("Hello, world!")
    return True
    
class Example:
    def __init__(self):
        self.value = 42
        
# This is a comment
x = 10
if x > 5:
    print("x is greater than 5")
        """
        assert detect_format_type(content) == "code"

class TestSegmentation:
    """Tests for the text segmentation functionality."""
    
    def test_segment_plain_text_discourse(self):
        """Test segmenting plain text with discourse strategy."""
        content = """This is the first paragraph.
        
This is the second paragraph with more text.

And this is the third paragraph, which is a bit longer and has multiple sentences. 
It continues with more information. And it has even more sentences.

The fourth paragraph is also here."""
        
        segments = segment_response(content, strategy="discourse", format_type="plain")
        assert len(segments) == 4
        assert "first paragraph" in segments[0]
        assert "second paragraph" in segments[1]
        assert "third paragraph" in segments[2]
        assert "fourth paragraph" in segments[3]
        
    def test_segment_markdown(self):
        """Test segmenting markdown content."""
        content = """# Heading
        
This is a paragraph in markdown.

## Subheading

- List item 1
- List item 2

Another paragraph here.

```python
print("Code block")
```

Final paragraph."""
        
        segments = segment_markup(content)
        assert len(segments) > 3
        assert "# Heading" in segments[0]
        assert "paragraph in markdown" in segments[1]
        
    def test_segment_with_sentence_boundary(self):
        """Test segmenting text with sentence boundary strategy."""
        content = "This is the first sentence. This is the second sentence. And this is the third sentence."
        
        segments = segment_response(content, strategy="sentence_boundary", format_type="plain")
        assert len(segments) == 3
        assert "first sentence" in segments[0]
        assert "second sentence" in segments[1]
        assert "third sentence" in segments[2]

class TestFactualDetection:
    """Tests for the factual response detection."""
    
    def test_factual_response(self):
        """Test detecting factual responses."""
        factual_texts = [
            "The capital of France is Paris.",
            "2 + 2 = 4",
            "JavaScript was created in 1995.",
            "The Earth orbits the Sun.",
            "Python is a programming language."
        ]
        
        for text in factual_texts:
            assert is_factual_response(text) is True
            
    def test_non_factual_response(self):
        """Test detecting non-factual responses."""
        non_factual_texts = [
            "I think that might be a good idea.",
            "You could try using a different approach.",
            "Let me explain how this works.",
            "Here are some suggestions for your project.",
            "Consider implementing this feature in your application."
        ]
        
        for text in non_factual_texts:
            assert is_factual_response(text) is False 