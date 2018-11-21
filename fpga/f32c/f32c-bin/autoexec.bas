100 PRINT "autoexec.bas drawing filled circles"
110 VIDMODE 0
120 FOR I=1 TO 100
130 INK RND(256)
140 CIRCLE RND(511), RND(287), RND(100), 1
150 NEXT
160 REM SLEEP 2
200 REM EXEC "demo/galaga.bin"
210 REM EXEC "demo/synth100.bin"
220 REN EXEC "demo/test_pcf.bin"
230 EXEC "demo/test_mcp.bin"
