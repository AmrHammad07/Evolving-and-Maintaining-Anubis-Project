using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace Events_Management_System_Version_2._1.Models
{
    public class Event
    {
        //attributes 
        public int ID { get; set; }         //primary key 

        [Required]
        [MaxLength(100)]
        [Display(Name = "Title")]
        public string Title { get; set; }

        [Required]
        [MaxLength(300)]
        [Display(Name = "Partial Content")]
        public string partialContent { get; set; }

        [Required]
        [Display(Name = "Full Content")]
        public string fullContent { get; set; }

        [Required]
        [MaxLength(6)]
        [Display(Name = "Event Code")]
        public String Code { get; set; }

        [Display(Name = "Display Image")]
        public string image { get; set; }

        [Display(Name = "Added Date")]
        public DateTime Added_Date { get; set; }
    }
}