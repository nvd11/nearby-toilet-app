import cv2

top = cv2.imread('/home/gateman/.openclaw/workspace/all_id.png', cv2.IMREAD_UNCHANGED)
bot = cv2.imread('/home/gateman/.openclaw/workspace/all_sig.png', cv2.IMREAD_UNCHANGED)

print("ID shape:", top.shape if top is not None else "None")
print("Sig shape:", bot.shape if bot is not None else "None")

