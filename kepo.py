import zlib,base64
exec(zlib.decompress(base64.b64decode("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")))