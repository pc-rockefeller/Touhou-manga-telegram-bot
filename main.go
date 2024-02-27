package main

import (
	"log"
	"os"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func main() {
	bot, err := tgbotapi.NewBotAPI(os.Getenv("THBOT_TELEGRAM_API_TOKEN"))
	if err != nil {
		log.Panic(err)
	}

	jar := myjarr.myjar{}

	bot.Debug = true // TODO: remove

	log.Printf("Authorized on account %s", bot.Self.UserName)

	u := tgbotapi.NewUpdate(0) // TODO move
	u.Timeout = 60             // TODO move

	handleUpdate := func(update tgbotapi.Update) {
		if update.Message != nil && update.Message.Invoice != nil {
			return
		}

		if update.Message != nil {
			log.Printf("[%s] %s", update.Message.From.UserName, update.Message.Text)

			msg := tgbotapi.NewMessage(update.Message.Chat.ID, update.Message.Text)
			msg.ReplyToMessageID = update.Message.MessageID

			bot.Send(msg)
		}
	}

	updates := bot.GetUpdatesChan(u)

	for update := range updates {
		go handleUpdate(update)
	}
}
