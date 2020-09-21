mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT || 5000\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
