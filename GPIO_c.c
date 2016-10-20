http://falsinsoft.blogspot.in/2012/11/access-gpio-from-linux-user-space.html
https://www.kernel.org/doc/Documentation/gpio/sysfs.txt
Device Drivers  ---> GPIO Support  ---> /sys/class/gpio/... (sysfs interface)
/sys/class/gpio/
/sys/class/gpio/gpioN/
There are three kinds of entries in /sys/class/gpio:
   -	Control interfaces used to get userspace control over GPIOs;
   -	GPIOs themselves; and
   -	GPIO controllers ("gpio_chip" instances).


echo XX > /sys/class/gpio/export
/sys/class/gpio/gpioXX/

echo "out" > /sys/class/gpio/gpioXX/direction
echo "in" > /sys/class/gpio/gpioXX/direction
echo 1 > /sys/class/gpio/gpioXX/value
echo 0 > /sys/class/gpio/gpioXX/value

cat /sys/class/gpio/gpioXX/value
echo XX > /sys/class/gpio/unexport

Kernel configuration ---> Kernel hacking ---> Debug FS
mount -t debugfs none /sys/kernel/debug
cat /sys/kernel/debug/gpio

int fd;
char buf[MAX_BUF]; 
int gpio = XX;
fd = open("/sys/class/gpio/export", O_WRONLY);
sprintf(buf, "%d", gpio); 
write(fd, buf, strlen(buf));
close(fd);

sprintf(buf, "/sys/class/gpio/gpio%d/direction", gpio);
fd = open(buf, O_WRONLY);
// Set out direction
write(fd, "out", 3); 
// Set in direction
write(fd, "in", 2); 
close(fd);


sprintf(buf, "/sys/class/gpio/gpio%d/value", gpio);
fd = open(buf, O_WRONLY);
// Set GPIO high status
write(fd, "1", 1); 
// Set GPIO low status 
write(fd, "0", 1); 
close(fd);


char value;

sprintf(buf, "/sys/class/gpio/gpio%d/value", gpio);

fd = open(buf, O_RDONLY);
read(fd, &value, 1);
if(value == '0')
{ 
     // Current GPIO status low
}
else
{
     // Current GPIO status high
}
close(fd);


fd = open("/sys/class/gpio/unexport", O_WRONLY);
sprintf(buf, "%d", gpio);
write(fd, buf, strlen(buf));
close(fd);


