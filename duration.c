#include <stdio.h>
#include <libavformat/avformat.h>

int main(int argc, char *argv[]) 
{
    if (argc < 2) 
    {
        printf("Usage: %s <video file>\n", argv[0]);
        return -1;
    }

    int i;
    unsigned long long int hours, mins, secs, us;
    int64_t duration;
    char *filename;
    
    hours = mins = secs = us = 0;
    
    for(i = 1; i < argc; i++)
    {
        filename = argv[i];

        AVFormatContext *formatContext = NULL;

        // Open video file
        if (avformat_open_input(&formatContext, filename, NULL, NULL) != 0) 
        {
            fprintf(stderr, "Could not open file %s\n", filename);
            continue;
        }

        // Retrieve stream information
        if (avformat_find_stream_info(formatContext, NULL) < 0) 
        {
            fprintf(stderr, "Could not find stream information\n");
            avformat_close_input(&formatContext);
            continue;
        }

        // Print detailed information about the file
        //av_dump_format(formatContext, 0, filename, 0);

        // Get the duration in seconds
        if (formatContext->duration != AV_NOPTS_VALUE) 
        {
            duration = formatContext->duration + (formatContext->duration <= INT64_MAX - 5000 ? 5000 : 0);
            secs += duration / AV_TIME_BASE;
            us += duration % AV_TIME_BASE;
        }

        // Close the video file
        avformat_close_input(&formatContext);
    }

    secs += us / AV_TIME_BASE;
    us = us % AV_TIME_BASE;
    mins = secs / 60;
    secs %= 60;
    hours = mins / 60;
    mins %= 60;

    printf("Total duration: %02llu hour(s) %02llu minute(s) %02llu second(s)\n", hours, mins, secs);


    return 0;
}
