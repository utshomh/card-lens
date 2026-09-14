from app.parser import parse_card_text


sample = """
John Smith
ABC Technologies Ltd
CEO
+880171234567
john@abc.com
www.abctech.com
"""


result = parse_card_text(sample)

print(result)