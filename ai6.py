* { box-sizing: border-box; }
body { font-family: Arial, Helvetica, sans-serif; background: #f4f4f4; color: #222; margin: 0; }
header { background: #1f3a5f; color: #fff; padding: 18px 24px; }
header h1 { margin: 0 0 4px; font-size: 22px; }
header p { margin: 0; font-size: 13px; opacity: .85; }
main { max-width: 760px; margin: 20px auto; padding: 0 14px; }
.card { background: #fff; border: 1px solid #ccc; border-radius: 6px; padding: 16px; margin-bottom: 16px; }
.card h2 { margin-top: 0; font-size: 18px; }
button { padding: 8px 16px; border: 1px solid #1f3a5f; background: #1f3a5f; color: #fff;
         border-radius: 4px; cursor: pointer; font-size: 14px; }
button:disabled { background: #999; border-color: #999; cursor: not-allowed; }
#stopBtn { background: #fff; color: #1f3a5f; }
.banner { padding: 8px 12px; border-radius: 4px; background: #e8e8e8; font-size: 13px; margin-bottom: 14px; }
.banner.warn { background: #fff3cd; border: 1px solid #e0c36a; }
.banner.ok { background: #d9efd9; border: 1px solid #8cc58c; }
.risk { font-size: 24px; font-weight: bold; text-align: center; padding: 12px; border-radius: 4px; color: #fff; }
.risk.none { background: #888; } .risk.LOW { background: #2e8b57; }
.risk.MEDIUM { background: #d98e04; } .risk.HIGH { background: #c0392b; }
.bar { height: 14px; background: #ddd; border-radius: 7px; margin: 12px 0; overflow: hidden; }
#barFill { height: 100%; width: 0; background: #2e8b57; transition: width .3s, background .3s; }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
th, td { border: 1px solid #ccc; padding: 6px; text-align: center; }
th { background: #eee; }
.note { font-size: 12px; color: #555; }
#liveStatus { margin-left: 10px; font-size: 13px; color: #555; }