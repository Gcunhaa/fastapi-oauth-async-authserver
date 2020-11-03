#! /usr/bin/env sh

echo "Starting migrations:"
 
# Run migrations
alembic upgrade head
