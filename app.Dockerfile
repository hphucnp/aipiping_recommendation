FROM python:3.12.3

# Update the package list
RUN apt-get update

# Install ping
RUN apt-get install -y iputils-ping

ENV WORKDIR /ai_piping
ENV CURRENT_APP app
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=$WORKDIR

WORKDIR $WORKDIR

COPY *requirements.txt $WORKDIR/
RUN pip install -r ${CURRENT_APP}.requirements.txt

COPY . .

RUN chmod +x ./${CURRENT_APP}/scripts/entrypoint.sh
ENTRYPOINT ["bash", "-c", "./${CURRENT_APP}/scripts/entrypoint.sh"]