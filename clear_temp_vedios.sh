GREEN='\033[0;32m'
NC='\033[0m' # No Color
TARGET="./media/videos/1080p60/partial_movie_files"
if [ -d "$TARGET" ]; then
    sudo rm -rfv "$TARGET"/*
    echo -e "${GREEN}Temporary video files cleared.${NC}"
else
    echo -e "\033[0;31mTarget folder not found!${NC}"
fi