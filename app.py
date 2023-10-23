import gradio as gr
import csv
import json
import io
import base64

def filter_by_key(data, filter_key, filter_value):
    filtered_data = [item for item in data if item.get(filter_key) == filter_value]
    return filtered_data

def json_to_csv(input_json, filter_key, filter_value):
    try:
        data = json.loads(input_json)
        filtered_data = filter_by_key(data, filter_key, filter_value)

        if filtered_data:
            fieldnames = list(set(key for item in filtered_data for key in item))
            output_csv = io.StringIO()
            writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_data)
            b64 = base64.b64encode(output_csv.getvalue().encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="filtered_data.csv">Download CSV file</a>'
            return href

        else:
            return "No data found matching the filter criteria."

    except Exception as e:
        error_message = f"Error: {str(e)}"
        return error_message

iface = gr.Interface(
    fn=json_to_csv,
    inputs=["text", "text", "text"],
    outputs="html",
    title="JSON to CSV Converter",
    description="Convert JSON data to CSV by filtering based on a specified key and value."
)

iface.launch(share=True, inbrowser=True)
