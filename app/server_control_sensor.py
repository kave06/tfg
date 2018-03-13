try:
    from app.model.receiver import connect_queue
    from app.modules.logger import create_log
except ImportError:
    from model.receiver import connect_queue
    from modules.logger import create_log

logger = create_log('prototype')


def main():
    channel = connect_queue()
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()
