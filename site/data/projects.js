// Project cards are data, not page layout. Add/reorder entries to change the site.
export const projects = [
  {
    id: "byebye-tgws-proxy",
    title: "ByeBye TGWS Proxy",
    category: "ANDROID / OPEN SOURCE",
    description: {
      ru: "Android-приложение, объединяющее локальный MTProto-прокси для Telegram и нативный обход DPI. Два независимых инструмента в одном интерфейсе, без root.",
      en: "An Android app combining a local MTProto proxy for Telegram and native DPI circumvention. Two independent tools in one interface, no root required."
    },
    links: [
      { id: "source", url: "https://github.com/Derigava/tg-ws-proxy-android" },
      { id: "release", url: "https://github.com/Derigava/tg-ws-proxy-android/releases/latest" }
    ]
  }
];
