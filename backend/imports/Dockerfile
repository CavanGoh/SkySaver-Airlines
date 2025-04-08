FROM alpine:latest

RUN apk add --no-cache curl tar

# Install decK binary
RUN curl -L https://github.com/kong/deck/releases/download/v1.46.2/deck_1.46.2_linux_amd64.tar.gz -o deck.tar.gz \
    && tar -xzf deck.tar.gz \
    && mv deck /usr/local/bin/deck \
    && chmod +x /usr/local/bin/deck

# Copy config and wait script
COPY kong.yaml /config/kong.yaml
COPY wait-for-kong.sh /wait-for-kong.sh
RUN chmod +x /wait-for-kong.sh

CMD ["/wait-for-kong.sh"]
