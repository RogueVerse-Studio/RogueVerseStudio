param(
  [Parameter(Mandatory = $true)][string]$Source,
  [Parameter(Mandatory = $true)][string]$OutputDirectory
)

Add-Type -AssemblyName System.Drawing

$targetWidth = 1080
$targetHeight = 1920
$orange = [System.Drawing.Color]::FromArgb(255, 255, 111, 0)
$white = [System.Drawing.Color]::White
$muted = [System.Drawing.Color]::FromArgb(255, 205, 221, 235)
$panel = [System.Drawing.Color]::FromArgb(222, 4, 10, 22)
$shadow = [System.Drawing.Color]::FromArgb(170, 0, 0, 0)
$fontPath = 'C:\Windows\Fonts\bahnschrift.ttf'
$boldFontPath = 'C:\Windows\Fonts\bahnschrift.ttf'

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$sourceImage = [System.Drawing.Image]::FromFile($Source)

$cards = @(
  @{ File = '01-chaos-breaker-is-coming.jpg'; Eyebrow = 'MUSHOKU TENSEI'; Title = "CHAOS BREAKER`nIS COMING"; Body = 'Season 3 enters its next major arc.'; Zoom = 1.00; CenterY = 0.50 },
  @{ File = '02-new-trailer.jpg'; Eyebrow = 'NEW TRAILER'; Title = "THE FIRST DEDICATED`nPREVIEW IS HERE"; Body = 'The Chaos Breaker Arc moves into view.'; Zoom = 1.08; CenterY = 0.43 },
  @{ File = '03-august-16.jpg'; Eyebrow = 'MARK THE DATE'; Title = 'AUGUST 16, 2026'; Body = 'The new storyline begins with Season 3, Episode 8.'; Zoom = 1.15; CenterY = 0.40 },
  @{ File = '04-world-getting-bigger.jpg'; Eyebrow = 'THE SCALE SHIFTS'; Title = "THE WORLD IS`nGETTING BIGGER"; Body = 'Rudeus moves deeper into the powers, history and mysteries behind his world.'; Zoom = 1.22; CenterY = 0.36 },
  @{ File = '05-new-cast.jpg'; Eyebrow = 'THREE CAST ADDITIONS'; Title = "NEW NAMES ENTER`nTHE BOARD"; Body = 'Perugius, Sylvaril and Atofe join the Season 3 ensemble.'; Zoom = 1.30; CenterY = 0.34 },
  @{ File = '06-spoiler-warning.jpg'; Eyebrow = 'ANIME-ONLY WARNING'; Title = "WATCH THE`nSPOILERS"; Body = 'Even an innocent Chaos Breaker search can reveal major light-novel details.'; Zoom = 1.38; CenterY = 0.32 },
  @{ File = '07-chaos-breaker-begins.jpg'; Eyebrow = 'THE FULL REVEAL'; Title = "CHAOS BREAKER`nBEGINS AUGUST 16"; Body = 'Are you ready? Follow RogueVerse Media for more anime news.'; Zoom = 1.05; CenterY = 0.40 }
)

function Draw-WrappedText {
  param(
    [System.Drawing.Graphics]$Graphics,
    [string]$Text,
    [System.Drawing.Font]$Font,
    [System.Drawing.Brush]$Brush,
    [float]$X,
    [float]$Y,
    [float]$Width,
    [float]$LineHeight
  )

  $cursorY = $Y
  foreach ($paragraph in ($Text -split "`n")) {
    $words = $paragraph -split '\s+'
    $line = ''
    foreach ($word in $words) {
      $candidate = if ($line) { "$line $word" } else { $word }
      if ($Graphics.MeasureString($candidate, $Font).Width -gt $Width -and $line) {
        $Graphics.DrawString($line, $Font, $Brush, $X, $cursorY)
        $cursorY += $LineHeight
        $line = $word
      } else {
        $line = $candidate
      }
    }
    if ($line) {
      $Graphics.DrawString($line, $Font, $Brush, $X, $cursorY)
      $cursorY += $LineHeight
    }
  }
  return $cursorY
}

foreach ($card in $cards) {
  $bitmap = New-Object System.Drawing.Bitmap($targetWidth, $targetHeight)
  $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
  $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
  $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
  $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

  $cropWidth = [int]($sourceImage.Width / $card.Zoom)
  $cropHeight = [int]($sourceImage.Height / $card.Zoom)
  $cropX = [int](($sourceImage.Width - $cropWidth) / 2)
  $centerY = [int]($sourceImage.Height * $card.CenterY)
  $cropY = [Math]::Max(0, [Math]::Min($sourceImage.Height - $cropHeight, $centerY - [int]($cropHeight / 2)))
  $sourceRect = New-Object System.Drawing.Rectangle($cropX, $cropY, $cropWidth, $cropHeight)
  $destRect = New-Object System.Drawing.Rectangle(0, 0, $targetWidth, $targetHeight)
  $graphics.DrawImage($sourceImage, $destRect, $sourceRect, [System.Drawing.GraphicsUnit]::Pixel)

  $gradientRect = New-Object System.Drawing.Rectangle(0, 0, $targetWidth, 640)
  $gradient = New-Object System.Drawing.Drawing2D.LinearGradientBrush($gradientRect, $shadow, [System.Drawing.Color]::Transparent, 90)
  $graphics.FillRectangle($gradient, $gradientRect)
  $gradient.Dispose()

  $panelRect = New-Object System.Drawing.Rectangle(0, 1260, $targetWidth, 660)
  $panelBrush = New-Object System.Drawing.SolidBrush($panel)
  $graphics.FillRectangle($panelBrush, $panelRect)
  $panelBrush.Dispose()

  $orangeBrush = New-Object System.Drawing.SolidBrush($orange)
  $whiteBrush = New-Object System.Drawing.SolidBrush($white)
  $mutedBrush = New-Object System.Drawing.SolidBrush($muted)
  $brandFont = New-Object System.Drawing.Font('Bahnschrift', 32, [System.Drawing.FontStyle]::Bold)
  $eyebrowFont = New-Object System.Drawing.Font('Bahnschrift', 34, [System.Drawing.FontStyle]::Bold)
  $titleSize = if ($card.Title.Length -gt 34) { 60 } else { 68 }
  $titleFont = New-Object System.Drawing.Font('Bahnschrift', $titleSize, [System.Drawing.FontStyle]::Bold)
  $bodyFont = New-Object System.Drawing.Font('Segoe UI', 36, [System.Drawing.FontStyle]::Regular)
  $footerFont = New-Object System.Drawing.Font('Segoe UI', 23, [System.Drawing.FontStyle]::Regular)

  $graphics.FillRectangle($orangeBrush, 58, 62, 16, 66)
  $graphics.DrawString('ROGUEVERSE NEWS', $brandFont, $whiteBrush, 96, 73)
  $graphics.DrawString($card.Eyebrow, $eyebrowFont, $orangeBrush, 68, 1310)
  $titleBottom = Draw-WrappedText -Graphics $graphics -Text $card.Title -Font $titleFont -Brush $whiteBrush -X 64 -Y 1370 -Width 950 -LineHeight 82
  Draw-WrappedText -Graphics $graphics -Text $card.Body -Font $bodyFont -Brush $mutedBrush -X 68 -Y ($titleBottom + 25) -Width 930 -LineHeight 48 | Out-Null
  $graphics.DrawString('ROGUEVERSEMEDIA.COM', $brandFont, $orangeBrush, 68, 1830)
  $copyright = 'Original artwork created for RogueVerse Media'
  $copyrightWidth = $graphics.MeasureString($copyright, $footerFont).Width
  $graphics.DrawString($copyright, $footerFont, $mutedBrush, $targetWidth - $copyrightWidth - 58, 1872)

  $encoder = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object MimeType -eq 'image/jpeg'
  $qualityEncoder = [System.Drawing.Imaging.Encoder]::Quality
  $parameters = New-Object System.Drawing.Imaging.EncoderParameters(1)
  $parameters.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter($qualityEncoder, 94L)
  $bitmap.Save((Join-Path $OutputDirectory $card.File), $encoder, $parameters)

  $parameters.Dispose()
  $brandFont.Dispose(); $eyebrowFont.Dispose(); $titleFont.Dispose(); $bodyFont.Dispose(); $footerFont.Dispose()
  $orangeBrush.Dispose(); $whiteBrush.Dispose(); $mutedBrush.Dispose()
  $graphics.Dispose(); $bitmap.Dispose()
}

$hero = New-Object System.Drawing.Bitmap(1672, 941)
$heroGraphics = [System.Drawing.Graphics]::FromImage($hero)
$heroGraphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$heroCropHeight = [int]($sourceImage.Width * 941 / 1672)
$heroCropY = 100
$heroGraphics.DrawImage($sourceImage, (New-Object System.Drawing.Rectangle(0, 0, 1672, 941)), (New-Object System.Drawing.Rectangle(0, $heroCropY, $sourceImage.Width, $heroCropHeight)), [System.Drawing.GraphicsUnit]::Pixel)
$heroEncoder = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object MimeType -eq 'image/jpeg'
$heroParameters = New-Object System.Drawing.Imaging.EncoderParameters(1)
$heroParameters.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, 92L)
$hero.Save((Join-Path $OutputDirectory 'chaos-breaker-hero.jpg'), $heroEncoder, $heroParameters)
$heroParameters.Dispose(); $heroGraphics.Dispose(); $hero.Dispose(); $sourceImage.Dispose()
