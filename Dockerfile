FROM python:3.9

WORKDIR /obj_detection

COPY ./requirements.txt /obj_detection/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r /obj_detection/requirements.txt

# Copy the entire application code to the working directory
# COPY . .

# Set the command to run your application
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["/bin/sh", "-c", "bash"]