import { axios } from "@pipedream/platform"

export default defineComponent({
  props: {
    data: { type: "data_store" },
  },
  async run({ steps, $ }) {
    const webhookUrl = "https://discord.com/api/webhooks/1494834782402514946/DeXK76KOMyEED4cF-uqtxcXEhepk8-3PBNch9SKEilwkgBcL37H9oxk3mr0SITCWnyHn";
    
    // Haetaan alkuperäiset kentät BattleMetrics-viestistä
    const b = steps.trigger.event.body.embeds[0];
    const f = b.fields;

    // Luodaan uusi viesti englanninkielisillä otsikoilla
    const payload = {
      embeds: [{
        title: "Server Status",
        color: 5814783,
        fields: [
          { name: "Server Name", value: f[0].value },
          { name: "Status", value: f[1].value, inline: true },
          { name: "Players", value: f[2].value, inline: true },
          { name: "Map", value: f[3].value }
        ],
        image: {
          url: "https://cdn.discordapp.com/attachments/1494851993154490448/1494852038797037681/5thmrlogo.gif?ex=69e41cf3&is=69e2cb73&hm=34113ebf686b927466e7b834a97188059ac0f84c63dbdf9440534c1d20be5d4a&"
        },
        footer: { text: "Updated" },
        timestamp: new Date()
      }]
    };

    let messageId = await this.data.get("discord_message_id");

    if (!messageId) {
      const response = await axios($, {
        method: "POST",
        url: `${webhookUrl}?wait=true`,
        data: payload,
      });
      await this.data.set("discord_message_id", response.id);
      return "New message created!";
    } else {
      try {
        await axios($, {
          method: "PATCH",
          url: `${webhookUrl}/messages/${messageId}`,
          data: payload,
        });
        return "Message updated!";
      } catch (error) {
        await this.data.set("discord_message_id", null);
        return "Message not found, ID reset.";
      }
    }
  },
})
