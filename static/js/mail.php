<?php
    $to = "botrasp@yandex.ru";
    $name = $_POST['name'];
    $email = $_POST['email'];
    $subject = $_POST["subject"];

    $message = '
    <html>
    <body>
    <center>
    <table border=1 cellpadding=6 cellspacing=0 width=90% bordercolor="#DBDBDB">
     <tr><td colspan=2 align=center bgcolor="#E4E4E4"><b>Информация</b></td></tr>
     <tr>
      <td><b>От кого</b></td>
      <td>'.$name.'</td>
     </tr>
     <tr>
      <td><b>Почта</b></td>
      <td><a href="mailto:'.$email.'">'.$email.'</a></td>
     </tr>
     <tr>
      <td><b>Тема</b></td>
      <td>'.$subject.'</td>
     </tr>
     <tr>
      <td><b>Сообщение</b></td>
      <td>'.$_POST['message'].'</td>
     </tr>
    </table>
    </center>
    </body>
    </html>';
    $headers  = "Content-type: text/html; charset=utf-8\r\n";
    if (filter_var($email, FILTER_VALIDATE_EMAIL)){
        mail($to, $subject, $message, $headers);
    }
    else{
        echo 1;
    }
?>