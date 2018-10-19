FROM python:3-onbuild

EXPOSE 5000

CMD ["python", "./src/main_part.py"]