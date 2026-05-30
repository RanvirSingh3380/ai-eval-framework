import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.append(["content"])
ws.append(["Artificial Intelligence is transforming healthcare by enabling faster diagnosis and personalized treatment plans."])
ws.append(["Machine learning algorithms can detect patterns in large datasets that humans cannot see manually."])
ws.append(["Deep learning uses neural networks with multiple layers to process images, text, and speech."])
ws.append(["AI ethics focuses on ensuring AI systems are fair, transparent, and accountable to society."])

wb.save("dataset/test_data.xlsx")
print("Excel file created")